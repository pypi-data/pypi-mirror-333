from .cosg import indexByGene, iqrLogNormalize

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
import matplotlib.patheffects as PathEffects
from scipy.sparse import issparse


## Helper function
def _compute_gene_expression_percentage(adata, group_by, cosg_score_df, layer=None):
    """
    Computes the percentage of cells expressing genes in `cosg_score_df` within each cell type group.

    This optimized function calculates expression only for the genes present in `cosg_score_df`,
    making it significantly more efficient than computing for all genes.

    Parameters
    ----------
    adata : AnnData
        The AnnData object containing expression data.
    group_by : str
        The observation column in `adata.obs` to group cells.
    cosg_score_df : pd.DataFrame
        A DataFrame containing COSG scores, where index corresponds to marker genes.
    layer : str, optional (default: None)
        If provided, uses `adata.layers[layer]` for expression data; otherwise, uses `adata.X`.

    Returns
    -------
    pd.DataFrame
        A DataFrame where:
        - Rows correspond to genes.
        - Columns correspond to cell types.
        - Values represent the percentage of cells expressing the gene in that cell type.
    """

    # Get only the relevant genes that exist in adata
    genes_to_use = cosg_score_df.index.intersection(adata.var_names)
    if len(genes_to_use) == 0:
        raise ValueError("No valid genes from cosg_score_df are found in adata.var_names.")

    # Extract the relevant expression data
    expr_data = adata[:, genes_to_use].X if layer is None else adata[:, genes_to_use].layers[layer]

    # Convert to binary presence/absence (1 if expressed, 0 otherwise)
    if issparse(expr_data):
        expr_data = expr_data.copy()  # Ensure no modification of original data
        expr_data.data[:] = 1  # Convert all nonzero values to 1
    else:
        expr_data = (expr_data > 0).astype(int)

    # Convert to DataFrame (cells as rows, genes as columns)
    expr_df = pd.DataFrame(expr_data.toarray() if issparse(expr_data) else expr_data,
                           index=adata.obs_names, columns=genes_to_use)

    # Compute the sum of expressing cells for each group (vectorized)
    expr_sums = expr_df.groupby(adata.obs[group_by], observed=True).sum()  # ✅ Fix applied: observed=True

    # Compute percentage of expressing cells per group
    group_sizes = adata.obs[group_by].value_counts().reindex(expr_sums.index, fill_value=0).values
    expr_percentages = (expr_sums.div(group_sizes, axis=0) * 100).T  # Transpose so genes are rows

    return expr_percentages





# Radial layout helper function
def _build_subtree_sizes(G, node, subtree_size, visited):
    """
    Recursively compute the number of leaf descendants for each node.
    """
    if node in visited:
        return subtree_size[node]
    visited.add(node)
    children = list(G.successors(node))
    if len(children) == 0:
        subtree_size[node] = 1
    else:
        total = 0
        for c in children:
            total += _build_subtree_sizes(G, c, subtree_size, visited)
        subtree_size[node] = total
    return subtree_size[node]

def _radial_dendrogram_layout(G, root, radius_step=1.5, start_angle=0, end_angle=2*np.pi):
    """
    Compute a radial layout for a tree (with the root at the center).
    Angles are distributed in proportion to the number of leaf nodes.
    """
    subtree_size = {}
    _build_subtree_sizes(G, root, subtree_size, visited=set())
    pos = {}

    def recurse(node, r, alpha_start, alpha_end):
        alpha_mid = 0.5 * (alpha_start + alpha_end)
        pos[node] = (r * np.cos(alpha_mid), r * np.sin(alpha_mid))
        children = list(G.successors(node))
        if len(children) == 0:
            return
        total_leaves = sum(subtree_size[ch] for ch in children)
        r_next = r + radius_step
        angle_offset = alpha_start
        for ch in children:
            frac = subtree_size[ch] / total_leaves
            ch_alpha_start = angle_offset
            ch_alpha_end = angle_offset + frac * (alpha_end - alpha_start)
            recurse(ch, r_next, ch_alpha_start, ch_alpha_end)
            angle_offset = ch_alpha_end

    recurse(root, 0.0, start_angle, end_angle)
    return pos






### Plot marker specificity with cell type dendrogram information


def plotMarkerDendrogram(
    adata,
    group_by: str,
    use_rep: str = 'X_pca',
    calculate_dendrogram_on_cosg_scores: bool = True,
    top_n_genes: int = 3,
    cosg_key: str = 'cosg',
    radius_step: float = 1.5,
    cmap: str = "Purples",
    cell_type_label_offset: float = 0,
    gene_label_offset: float = 0.25,
    gene_label_color: str = None,
    linkage_method: str = "ward",
    distance_metric: str = "euclidean",
    hierarchy_merge_scale: float = None,
    collapse_scale: float = None,
    add_cluster_node_for_single_node_cluster : bool = True,
    palette=None,
    gene_color_min: float = 0,
    gene_color_max: float = None,
    font_outline: float = 2,
    figure_size: tuple = (10, 10),
    node_shape_cell_type: str = 'o',
    node_shape_gene: str = 's',
    node_shape_internal: str = 'o',
    colorbar_width: float = 0.01,
    layer: str = None,
    gene_size_scale: float = 300,
    map_cell_type_gene: dict = None,
    cell_type_selected: list = None,
    color_root_node: str = '#D6EFD5',
    color_internal_node: str = 'lightgray',
    color_edge: str = 'lightgray',
    edge_curved: float = 0.0,
    show_figure: bool = True,
    save: str = None,
):
    # Import matplotlib modules needed for curved edges
    import matplotlib.path as mpath
    import matplotlib.patches as mpatches
    """
    Visualizes a radial dendrogram of cell types with attached top marker genes.
    
    Computes a dendrogram in two modes:
    - If `calculate_dendrogram_on_cosg_scores` is True, uses COSG scores from `adata.uns['cosg']['COSG']`, 
      processed with `indexByGene()` and `iqrLogNormalize()`, then computes the dendrogram on the transposed DataFrame 
      with the specified `distance_metric` and `linkage_method`.
    - If False, aggregates `adata.obsm[use_rep]` by `adata.obs[group_by]`, computing distances with `pdist` 
      and linkage with the given `distance_metric` and `linkage_method`.

    When `collapse_scale` (0 to 1) is set and yields multiple clusters, cell types are grouped with cluster nodes; 
    if only one cluster, they attach directly to the root unless `add_cluster_node_for_single_node_cluster` is True, 
    which adds a cluster node for single-member clusters. If `collapse_scale` is None, `hierarchy_merge_scale` 
    (0 to 1) controls merging binary nodes into multi-child nodes based on distance similarity, with no merging 
    if None. Top marker genes (from COSG data) are added as nodes to cell type leaves, with labels offset by 
    `gene_label_offset` and colored by `gene_label_color` if provided.

    Cell type node colors come from `palette`:
    - Dictionary: Maps cell types to colors.
    - List: Assigns colors by cell type order.
    - None: Uses `adata.uns[f"{group_by}_colors"]` if available, else defaults to "lightblue".
    Marker gene node colors are scaled between `gene_color_min` and `gene_color_max` (max defaults to the 
    highest score). Node sizes reflect expression percentage (fraction of cells with expression > 0) from 
    `adata.X` or `adata.layers[layer]`.
    
    
    Parameters
    ----------
    adata : AnnData
        An AnnData object.
    group_by : str
        The observation key in adata.obs to group cell types.
    use_rep : str, optional, default='X_pca'
        The representation to use when aggregating data from adata.obsm.
    calculate_dendrogram_on_cosg_scores : bool, optional, default=True
        If True, compute the dendrogram on COSG scores derived using cosg.cosg, cosg.indexByGene and cosg.iqrLogNormalize.
        If False, compute the dendrogram on the aggregated representation from adata.obsm[use_rep].
    top_n_genes : int, optional, default=3
        Number of top marker genes (per cell type) to attach.
    cosg_key : str, optional, default='cosg'
        The key used to access the COSG marker gene identification results. Defaults to "cosg".
    radius_step : float, optional, default=1.5
        Radial distance between successive levels in the layout.
    cmap : str, optional, default="Purples"
        The matplotlib colormap to use for gene nodes.
    cell_type_label_offset : float, optional, default=0
        Fractional radial offset for cell type labels from the cell type node.
    gene_label_offset : float, optional, default=0.25
        Fractional radial offset for gene labels from the marker node.
    gene_label_color : str, optional, default=None
        If provided, this color is used for gene labels; otherwise, the gene node's colormap color is used.
    linkage_method : str, optional, default="ward"
        Linkage method to use when computing the dendrogram.
    distance_metric : str, optional, default="euclidean"
        Distance metric to use when computing the dendrogram.
    hierarchy_merge_scale : float or None, optional, default=None
        Controls the merging of binary nodes into multi-child nodes to simulate a non-binary hierarchy when
        collapse_scale is None. If provided, must be a float between 0 and 1, scaling the threshold relative to
        the range of linkage distances in Z. Nodes with distance differences below this scaled threshold are
        merged with their parent, allowing nodes to have more than two children.
        - 0: No merging (retains binary structure).
        - 1: Maximal merging (merges nodes if their distances differ by less than the full distance range).
        If None, no merging is performed, preserving the default binary dendrogram structure from Z.
        Raises ValueError if not between 0 and 1 when provided.
    collapse_scale : float or None, optional, default=None
        Controls the level of clustering in the dendrogram. If None, builds a full hierarchical dendrogram where
        nodes may have more than two children based on distance similarity. If a float between 0 and 1, scales the
        threshold relative to the min and max linkage distances in Z, collapsing leaves and internal nodes with
        distances below this scaled threshold into cluster nodes. 
        - 0: Maximal clustering (collapses at the minimum distance).
        - 1: Minimal clustering (collapses at the maximum distance).
        If only one cluster is found, no extra cluster node is added between the root and leaves. 
        Raises ValueError if not between 0 and 1 when provided.
    add_cluster_node_for_single_node_cluster : bool, optional, default=True
        Determines whether to create a cluster node for clusters containing only a single cell type when
        collapse_scale is provided. If True, a cluster node is added between the root and the single cell type
        node, maintaining a consistent hierarchy. If False, the single cell type node is connected directly to
        the root without an intermediate cluster node. Only applies when collapse_scale is not None and clustering
        results in single-member clusters.
    palette : dict, list, or None, optional, default=None
        Colors for cell type nodes. If a dict, keys are cell type names and values are colors.
        If a list, colors are assigned in order of cell types.
        If None and if adata.uns contains f"{group_by}_colors", that palette is used.
        Otherwise, cell type nodes default to "lightblue".
    gene_color_min : float, optional, default=0
        Minimum value for normalizing marker gene node colors.
    gene_color_max : float or None, optional, default=None
        Maximum value for normalizing marker gene node colors. If None, the maximum among marker scores is used.
    font_outline : float, optional, default=2
        Outline width for text labels.
    figure_size : tuple, optional, default=(10, 10)
        Size of the figure.
    node_shape_cell_type : str, optional, default='d'
        Shape of the cell type nodes. Default is 'd' (diamond). Can be any valid NetworkX node shape.
        Specification is as matplotlib.scatter marker, one of 'so^>v<dph8'. In detail:
        - 'o' : Circle
        - 's' : Square
        - 'd' : Diamond
        - 'v' : Triangle Down
        - '^' : Triangle Up
        - '<' : Triangle Left
        - '>' : Triangle Right
        - 'p' : Pentagon
        - 'h' : Hexagon
        - '8' : Octagon
    node_shape_gene : str, optional, default='o'
        Shape of marker gene nodes. Default is 'o' (circle).
    node_shape_internal : str, optional, default='o'
        Shape of internal dendrogram nodes. Default is 'o' (circle).
    colorbar_width : float, optional, default=0.01
        Width (in normalized figure coordinates) for the colorbar.
    layer : str, optional, default=None
        If provided, use adata.layers[layer] to calculate expression; otherwise, use adata.X.
    gene_size_scale : float, optional, default=300
        Base size for marker gene nodes; final size = gene_size_scale * (expression_percentage / 100).
    map_cell_type_gene : dict, optional, default=None
        Custom mapping of cell types to marker genes. If provided, this will be used instead of the top marker genes.
        Should be a dictionary where keys are cell type names and values are lists of gene names.
        Only genes present in adata.var_names will be included. It's okay if some cell types are not in the dict.
    cell_type_selected : list, optional, default=None
        List of cell types to include in the visualization. If provided, only these cell types will be shown.
        If None, all cell types will be included. Raises ValueError if none of the provided cell types are valid.
    color_root_node : str, optional, default='#D6EFD5'
        Color for the root node. Default is a dark gray (#404040).
    color_internal_node : str, optional, default='lightgray'
        Color for internal nodes and cluster nodes. Default is lightgray.
    color_edge : str, optional, default='lightgray'
        Color for all edges in the dendrogram. Default is lightgray.
    edge_curved : float, optional, default=0.0
        Controls the curvature of edges. 0.0 means straight lines, positive values increase curvature.
        Recommended range: 0.0 to 0.3. Default is 0.0 (straight lines).
    show_figure : bool, optional (default=True)
        Whether to display the figure after plotting.
    save : str or None, optional (default=None)
        File path to save the resulting figure. If None, the figure will not be saved.
    
    Returns
    -------
    None
        Displays a matplotlib figure of the radial dendrogram if `show_figure=True`.
    
    Example
    -------
    >>> import cosg
    >>> cosg.plotMarkerDendrogram(
    ...     adata,
    ...     group_by="CellTypes",
    ...     use_rep="X_pca",
    ...     calculate_dendrogram_on_cosg_scores=False,
    ...     top_n_genes=3,
    ...     radius_step=1.5,
    ...     cmap="Purples",
    ...     gene_label_offset=0.25,
    ...     gene_label_color="black",
    ...     linkage_method="ward",
    ...     distance_metric="correlation",
    ...     collapse_threshold=0.3,
    ...     palette=None,
    ...     gene_color_min=0,
    ...     gene_color_max=None,
    ...     font_outline=2,
    ...     figure_size=(10,10),
    ...     colorbar_width=0.02,
    ...     layer=None,
    ...     gene_size_scale=300
    ... )
    """
    # Compute the transformed COSG scores
    cosg_df = indexByGene(
        adata.uns[cosg_key]['COSG'],
        set_nan_to_zero=True,
        convert_negative_one_to_zero=True
    )
    cosg_score_df = iqrLogNormalize(cosg_df)
    
    # Decide which dendrogram to use
    if calculate_dendrogram_on_cosg_scores:
        data = cosg_score_df.T.values  # rows: cell types, columns: genes
        D = pdist(data, metric=distance_metric)
        Z = linkage(D, method=linkage_method)
        all_cell_types = list(cosg_score_df.columns)
    else:
        rep = adata.obsm[use_rep]
        df_rep = pd.DataFrame(rep, index=adata.obs_names)
        df_rep[group_by] = adata.obs[group_by].values
        group_means = df_rep.groupby(group_by, observed=True).mean()
        all_cell_types = list(group_means.index)
        data = group_means.values
        D = pdist(data, metric=distance_metric)
        Z = linkage(D, method=linkage_method)
    
    # Filter cell types if cell_type_selected is provided
    if cell_type_selected is not None:
        # Check which selected cell types are valid
        valid_selected_cell_types = [ct for ct in cell_type_selected if ct in all_cell_types]
        
        # If no valid cell types, raise an error
        if not valid_selected_cell_types:
            raise ValueError(f"None of the provided cell types {cell_type_selected} are valid. Valid cell types are: {all_cell_types}")
        
        # If only one valid cell type, we can't perform hierarchical clustering
        if len(valid_selected_cell_types) == 1:
            print(f"Only one valid cell type selected ({valid_selected_cell_types[0]}). Skipping hierarchical clustering.")
            # Set up a simplified tree with just one cell type
            G = nx.DiGraph()
            root = "root"
            G.add_node(root, node_type='root')
            
            ct = valid_selected_cell_types[0]
            G.add_node(ct, node_type='cell_type')
            G.add_edge(root, ct)
            
            # Update cell_types
            cell_types = valid_selected_cell_types
        else:
            # Create a mask for the distance matrix and linkage
            cell_type_indices = [all_cell_types.index(ct) for ct in valid_selected_cell_types]
            
            # Filter the data matrix
            if calculate_dendrogram_on_cosg_scores:
                filtered_data = cosg_score_df.iloc[:, [all_cell_types.index(ct) for ct in valid_selected_cell_types]].T.values
            else:
                filtered_data = group_means.iloc[[all_cell_types.index(ct) for ct in valid_selected_cell_types]].values
            
            # Recompute distances and linkage with filtered data
            D = pdist(filtered_data, metric=distance_metric)
            Z = linkage(D, method=linkage_method)
            
            # Update cell_types to only include selected ones
            cell_types = valid_selected_cell_types
    else:
        # Use all cell types
        cell_types = all_cell_types
    
    N = len(cell_types)
    
    # Check if we have at least two cell types for hierarchical clustering
    if N < 2:
        # We already handled the special case with only one selected cell type above,
        # but we'll keep this as a safety check for other code paths
        if 'G' not in locals():  # Only create the graph if not already created
            G = nx.DiGraph()
            root = "root"
            G.add_node(root, node_type='root')
            
            ct = cell_types[0]
            G.add_node(ct, node_type='cell_type')
            G.add_edge(root, ct)
    else:
        ### Build the tree graph
        G = nx.DiGraph()

        # Validate collapse_scale if provided
        if collapse_scale is not None:
            if not (0 <= collapse_scale <= 1):
                raise ValueError("collapse_scale must be between 0 and 1")

        # Validate hierarchy_merge_scale if provided
        if collapse_scale is None and hierarchy_merge_scale is not None:
            if not (0 <= hierarchy_merge_scale <= 1):
                raise ValueError("hierarchy_merge_scale must be between 0 and 1")

        # Calculate the range of distances in Z for scaling
        distances = Z[:, 2]  # Third column of Z contains the distances
        min_dist = np.min(distances)
        max_dist = np.max(distances)
        dist_range = max_dist - min_dist
        if collapse_scale is not None:
            if collapse_scale==0:
                scaled_collapse_threshold = min_dist - 1e-6
            else:
                # Scale the collapse_scale (0 to 1) to the actual distance range
                scaled_collapse_threshold = min_dist + collapse_scale * dist_range if dist_range > 0 else min_dist
        

        if collapse_scale is None:
            # Full hierarchical structure (not strictly binary)
            from collections import defaultdict
            # Track nodes and their children
            node_children = defaultdict(list)
            node_types = {}

            # Add cell types as leaf nodes
            for ct in cell_types:
                G.add_node(ct, node_type='cell_type')
                node_types[ct] = 'cell_type'

            # Process the linkage matrix Z to build the hierarchy
            for i, row in enumerate(Z):
                left_idx, right_idx, distance, _ = row
                left_idx, right_idx = int(left_idx), int(right_idx)
                internal_node = f"internal_{i+N}"
                G.add_node(internal_node, node_type='internal')
                node_types[internal_node] = 'internal'

                # Identify children (could be leaf or internal nodes)
                left_node = cell_types[left_idx] if left_idx < N else f"internal_{left_idx}"
                right_node = cell_types[right_idx] if right_idx < N else f"internal_{right_idx}"

                # Add edges from parent to children
                G.add_edge(internal_node, left_node)
                G.add_edge(internal_node, right_node)

                # Store children for potential merging into multi-child nodes
                node_children[internal_node].extend([left_node, right_node])

            # Root is the last internal node
            root = f"internal_{2*N - 2}"
            
            # Mark this node specifically as root_internal to apply the root color
            G.nodes[root]['node_type'] = 'root_internal'

            # Optional: Collapse binary nodes into multi-child nodes (simulating non-binary hierarchy)
            if hierarchy_merge_scale is not None:
                # Scale the hierarchy_merge_scale to the distance range
                merge_threshold = hierarchy_merge_scale * dist_range if dist_range > 0 else 0
                distance_dict = {f"internal_{i+N}": row[2] for i, row in enumerate(Z)}
                for node in list(G.nodes()):
                    if node_types.get(node) == 'internal' and len(node_children[node]) == 2:
                        parent = next(iter(G.predecessors(node)), None)
                        if parent and abs(distance_dict.get(node, 0) - distance_dict.get(parent, 0)) < merge_threshold:
                            # Merge with parent if distances are within the scaled threshold
                            children = node_children[node]
                            G.remove_node(node)
                            for child in children:
                                G.add_edge(parent, child)
                            node_children[parent].extend(children)
                            node_children.pop(node)

        else:
            from collections import defaultdict
            # Use the scaled threshold in fcluster
            cluster_labels = fcluster(Z, t=scaled_collapse_threshold, criterion='distance')
            unique_clusters = np.unique(cluster_labels)
            root = "root"
            G.add_node(root, node_type='root')
            clusters = defaultdict(list)
            for ct, lbl in zip(cell_types, cluster_labels):
                clusters[lbl].append(ct)
            if len(unique_clusters) == 1:
                for ct in clusters[unique_clusters[0]]:
                    G.add_node(ct, node_type='cell_type')
                    G.add_edge(root, ct)
            else:
                for lbl, members in clusters.items():
                    if len(members) > 1:
                        cluster_node = f"cluster_{lbl}"
                        G.add_node(cluster_node, node_type='cluster')
                        G.add_edge(root, cluster_node)
                        for ct in members:
                            G.add_node(ct, node_type='cell_type')
                            G.add_edge(cluster_node, ct)
                    else:
                        if add_cluster_node_for_single_node_cluster:
                            cluster_node = f"cluster_{lbl}"
                            G.add_node(cluster_node, node_type='cluster')
                            G.add_edge(root, cluster_node)
                            ct = members[0]
                            G.add_node(ct, node_type='cell_type')
                            G.add_edge(cluster_node, ct)
                        else:
                            ct = members[0]
                            G.add_node(ct, node_type='cell_type')
                            G.add_edge(root, ct)
    
    # Check if a custom cell type to gene mapping is provided
    if map_cell_type_gene is not None:
        # Get a set of valid genes (those in adata.var_names)
        valid_genes = set(adata.var_names)
        
        # Dictionary to store selected genes for each cell type
        selected_genes_dict = {}
        all_selected_genes = set()
        
        # Process each cell type in the mapping
        mapped_cell_types = []
        for ct, genes in map_cell_type_gene.items():
            if ct not in cell_types:
                continue  # Skip cell types not in the data
            
            mapped_cell_types.append(ct)
            
            # Filter genes to keep only those in adata.var_names
            valid_ct_genes = [gene for gene in genes if gene in valid_genes]
            
            # Store the valid genes for this cell type
            selected_genes_dict[ct] = valid_ct_genes
            all_selected_genes.update(valid_ct_genes)
        
        # Check if there's any overlap between cell_types and mapped cell types
        if len(mapped_cell_types) == 0:
            if cell_type_selected is not None:
                raise ValueError(f"No overlap between cell types in map_cell_type_gene {list(map_cell_type_gene.keys())} and the selected cell types {cell_type_selected}")
            else:
                raise ValueError(f"None of the cell types in map_cell_type_gene {list(map_cell_type_gene.keys())} are present in the data")
        
        # Convert set to list for further processing
        selected_genes = list(all_selected_genes)
    else:
        # Extract top N marker genes for all cell types at once (original behavior)
        marker_genes_df = pd.DataFrame(adata.uns[cosg_key]['names']).iloc[:top_n_genes]  # Slice once for efficiency
        
        # Filter to only include selected cell types if needed
        if cell_type_selected is not None:
            cols_to_keep = [col for col in marker_genes_df.columns if col in valid_selected_cell_types]
            marker_genes_df = marker_genes_df[cols_to_keep]
        
        selected_genes = marker_genes_df.values.flatten()  # Flatten to get all genes as a 1D list
        selected_genes = pd.Index(selected_genes).dropna().unique()  # Remove NaNs & duplicates


    # Attach marker gene nodes to each cell type leaf
    gene_nodes = {}
    
    if map_cell_type_gene is not None:
        # Use the custom mapping
        for ct in cell_types:
            if ct not in G or ct not in selected_genes_dict or not selected_genes_dict[ct]:
                continue
            
            # Get the custom genes for this cell type
            ct_genes = selected_genes_dict[ct]
            
            for gene in ct_genes:
                marker_node = f"{ct}__gene__{gene}"
                # Get the COSG score if available, otherwise use 0
                score = cosg_score_df.loc[gene, ct] if gene in cosg_score_df.index and ct in cosg_score_df.columns else 0
                G.add_node(marker_node, node_type='gene', score=score, gene=gene)
                G.add_edge(ct, marker_node)
                gene_nodes[marker_node] = score
    else:
        # Original behavior using top marker genes
        marker_genes_df = pd.DataFrame(adata.uns[cosg_key]['names']).iloc[:top_n_genes]
        
        # Filter to only include selected cell types if needed
        if cell_type_selected is not None:
            cols_to_keep = [col for col in marker_genes_df.columns if col in valid_selected_cell_types]
            marker_genes_df = marker_genes_df[cols_to_keep]
        
        for ct in cell_types:
            if ct not in G or ct not in marker_genes_df.columns:
                continue

            # Get precomputed top N marker genes for this cell type
            top_genes = marker_genes_df[ct].dropna()  # Drop NaNs to avoid issues

            for gene in top_genes:
                marker_node = f"{ct}__gene__{gene}"
                score = cosg_score_df.loc[gene, ct] if gene in cosg_score_df.index else 0  # Fetch COSG score
                G.add_node(marker_node, node_type='gene', score=score, gene=gene)
                G.add_edge(ct, marker_node)
                gene_nodes[marker_node] = score
 

    
    ### Calculate the expression percentage
    filtered_cosg_score_df = cosg_score_df.loc[selected_genes] if len(selected_genes) > 0 else cosg_score_df  # Keep only selected marker genes
    gene_expr_percentage = _compute_gene_expression_percentage(adata, group_by, filtered_cosg_score_df, layer=layer)

    
    gene_node_sizes = {}
    for n, d in G.nodes(data=True):
        if d.get('node_type') == 'gene':
            ct = n.split('__gene__')[0]
            gene_name = d['gene']
            percentage = gene_expr_percentage.loc[gene_name, ct] if gene_name in gene_expr_percentage.index else 0
            gene_node_sizes[n] = gene_size_scale * (percentage / 100)
    
    # Set final node sizes
    node_sizes = {}
    for n, d in G.nodes(data=True):
        ntype = d.get('node_type', '')
        if ntype in ['internal', 'root', 'root_internal', 'cluster']:
            node_sizes[n] = 50
        elif ntype == 'cell_type':
            node_sizes[n] = 600
        else:
            # Default size for any other node types
            node_sizes[n] = 100
            
    # Add gene node sizes separately (which use the expression percentage)
    for n, d in G.nodes(data=True):
        if d.get('node_type') == 'gene':
            node_sizes[n] = gene_node_sizes.get(n, 300)
    
    # Compute radial layout
    pos = _radial_dendrogram_layout(G, root, radius_step=radius_step)
    
    # Set palette for cell type nodes if not provided
    if palette is None and f"{group_by}_colors" in adata.uns:
        # If cell types are filtered, we need to filter the palette too
        if cell_type_selected is not None and f"{group_by}_colors" in adata.uns:
            all_palette = adata.uns[f"{group_by}_colors"]
            all_categories = adata.obs[group_by].cat.categories
            
            # Create a filtered palette
            if len(all_palette) == len(all_categories):
                filtered_indices = [list(all_categories).index(ct) for ct in valid_selected_cell_types if ct in all_categories]
                palette = [all_palette[i] for i in filtered_indices]
            else:
                # Fallback if palette doesn't match categories
                palette = all_palette
        else:
            palette = adata.uns[f"{group_by}_colors"]
    
    # Drawing
    fig = plt.figure(figsize=figure_size)
    
    # Create a square main Axes for the network plot (slightly smaller to make room for legends)
    ax_main = fig.add_axes([0.05, 0.05, 0.75, 0.85])
    ax_main.set_aspect('equal')
    
    # Create legends on the right side
    legend_x = 0.82  # Common x position for legends
    
    # Create node type legend
    ax_ns = fig.add_axes([legend_x, 0.65, 0.15, 0.15])  # Node type legend at top
    
    # Create expression percentage legend
    ax_ds = fig.add_axes([legend_x, 0.525, 0.15, 0.15])  # Expression % legend in middle
    
    # Create colorbar Axes
    ax_cb = fig.add_axes([legend_x + 0.04, 0.15, colorbar_width, 0.25])  # Colorbar at bottom, shifted right

    ### Set up the color map for gene nodes
    cmap_obj = plt.get_cmap(cmap)
    if gene_nodes:
        scores_array = np.array(list(gene_nodes.values()))
        vmin = gene_color_min
        vmax = gene_color_max if gene_color_max is not None else scores_array.max()
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    else:
        norm = mcolors.Normalize(vmin=0, vmax=1)
    
    ### Setup the node colors
    node_colors = {}
    for n, d in G.nodes(data=True):
        ntype = d.get('node_type', '')
        if ntype == 'internal':
            node_colors[n] = color_internal_node
        elif ntype in ['root', 'root_internal']:  # Handle both explicit root and root_internal nodes
            node_colors[n] = color_root_node
        elif ntype == 'cluster':
            node_colors[n] = color_internal_node
        elif ntype == 'cell_type':
            if palette is not None:
                if isinstance(palette, dict):
                    node_colors[n] = palette.get(n, "lightblue")
                elif isinstance(palette, list):
                    try:
                        idx = cell_types.index(n)
                        node_colors[n] = palette[idx] if idx < len(palette) else "lightblue"
                    except ValueError:
                        node_colors[n] = "lightblue"
                else:
                    node_colors[n] = "lightblue"
            else:
                node_colors[n] = "lightblue"
        elif ntype == 'gene':
            node_colors[n] = cmap_obj(norm(d['score']))
        else:
            node_colors[n] = 'lightgrey'
            
    ### Setup the node shapes
    node_shapes = {}
    for n, d in G.nodes(data=True):
        ntype = d.get('node_type', '')
        if ntype == 'internal':
            node_shapes[n] = node_shape_internal
        elif ntype == 'cell_type':
            node_shapes[n] = node_shape_cell_type
        elif ntype == 'gene':
            node_shapes[n] = node_shape_gene
        else:
            node_shapes[n] = 'o'
    ### Draw nodes seprately, because they are using different shapes
    #### Draw cell type nodes with the specified shape
    node_list = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'cell_type']
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=node_list,
        node_shape=node_shape_cell_type,
        node_color=[node_colors[n] for n in node_list],
        node_size=[node_sizes[n] for n in node_list],
        ax=ax_main
    )
    
    #### Draw gene nodes with the specified shape
    node_list = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'gene']
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=node_list,
        node_shape=node_shape_gene,
        node_color=[node_colors[n] for n in node_list],
        node_size=[node_sizes[n] for n in node_list],
        ax=ax_main
    )
    
    #### Draw internal nodes with the specified shape
    node_list = [n for n, d in G.nodes(data=True) if d.get('node_type') not in ('gene', 'cell_type')]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=node_list,
        node_shape=node_shape_internal,
        node_color=[node_colors[n] for n in node_list],
        node_size=[node_sizes[n] for n in node_list],
        ax=ax_main
    )
    
    ### Draw edges:
    if edge_curved == 0:
        # Use the default straight edges
        nx.draw_networkx_edges(G, pos, ax=ax_main, arrows=False, edge_color=color_edge)
    else:
        # Draw curved edges
        for (u, v) in G.edges():
            # Get the start and end positions
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            
            # Create the curved connection
            # Calculate control point for quadratic bezier curve
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Calculate normal vector to the line connecting the nodes
            dx = x2 - x1
            dy = y2 - y1
            length = np.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                # Perpendicular vector with length scaled by edge_curved
                norm_x = -dy / length * edge_curved
                norm_y = dx / length * edge_curved
                
                # Control point by moving midpoint perpendicular to the line
                ctrl_x = mid_x + norm_x
                ctrl_y = mid_y + norm_y
                
                # Create a Path with a quadratic curve
                path = mpath.Path([(x1, y1), (ctrl_x, ctrl_y), (x2, y2)], [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3])
                patch = mpatches.PathPatch(path, fill=False, edgecolor=color_edge, lw=1)
                ax_main.add_patch(patch)
            else:
                # Fall back to straight line if points are the same
                ax_main.plot([x1, x2], [y1, y2], color=color_edge, lw=1)
    
    ### Plot the labels
    for n, d in G.nodes(data=True):
        if d.get('node_type') == 'gene':
            parents = list(G.predecessors(n))
            if not parents:
                continue
            parent = parents[0]
            x_parent, y_parent = pos[parent]
            x_gene, y_gene = pos[n]
            vec = np.array([x_gene - x_parent, y_gene - y_parent])
            norm_vec = vec / (np.linalg.norm(vec) + 1e-9)
            label_pos = (x_gene + gene_label_offset * norm_vec[0],
                         y_gene + gene_label_offset * norm_vec[1])
            angle = np.degrees(np.arctan2(norm_vec[1], norm_vec[0]))
            if angle > 90:
                angle -= 180
            elif angle < -90:
                angle += 180
            text_color = gene_label_color if gene_label_color is not None else node_colors[n]
            txt = ax_main.text(label_pos[0], label_pos[1], d['gene'],
                    fontsize=8, color=text_color,
                    rotation=angle,
                    horizontalalignment='center',
                    verticalalignment='center')
            txt.set_path_effects([PathEffects.withStroke(linewidth=font_outline, foreground='white')])
        ### Adjust the direction of cell type labels:
        elif d.get('node_type') == 'cell_type':
            parents = list(G.predecessors(n))
            if not parents:
                continue
            parent = parents[0]
            x_parent, y_parent = pos[parent]
            x_ct, y_ct = pos[n]
            vec = np.array([x_ct - x_parent, y_ct - y_parent])
            norm_vec = vec / (np.linalg.norm(vec) + 1e-9)
            label_pos = (x_ct + cell_type_label_offset * norm_vec[0],
                         y_ct + cell_type_label_offset * norm_vec[1])
            angle = np.degrees(np.arctan2(norm_vec[1], norm_vec[0]))
            if angle > 90:
                angle -= 180
            elif angle < -90:
                angle += 180
            txt = ax_main.text(label_pos[0], label_pos[1], n,
                               fontsize=10, color='black',
                               rotation=angle,
                               horizontalalignment='center',
                               verticalalignment='center')
            txt.set_path_effects([PathEffects.withStroke(linewidth=font_outline, foreground='white')])
    
    ### Set up the color bar
    sm = plt.cm.ScalarMappable(cmap=cmap_obj, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=ax_cb, orientation='vertical')
    # Move the label to the left side of the colorbar
    cbar.set_label("COSG Score", fontsize=12, rotation=270, labelpad=15, ha='center')
    
    
    ### Calculate the dot size dynamically
    min_expr = gene_expr_percentage[gene_expr_percentage > 0].min().min() if not gene_expr_percentage.empty else 5  # Ignore 0% values
    max_expr = gene_expr_percentage.max().max() if not gene_expr_percentage.empty else 100  # Maximum expression percentage

    # Round min/max to nearest multiple of 5
    min_expr_rounded = np.floor(min_expr / 5) * 5
    max_expr_rounded = np.ceil(max_expr / 5) * 5

    # Generate up to 5 evenly spaced values, ignoring 0%
    num_circles = min(5, int((max_expr_rounded - min_expr_rounded) / 5) + 1)
    legend_percentages = np.linspace(min_expr_rounded, max_expr_rounded, num=num_circles)
    legend_percentages = np.unique(np.round(legend_percentages / 5) * 5).astype(int)  # Ensure multiples of 5

    # Generate dot size legend (skip 0%)
    legend_markers = [
        plt.Line2D([0], [0], marker=node_shape_gene, color='black', label=f' {p}%', 
                   markerfacecolor='white', markersize=np.sqrt(gene_size_scale * (p/100)))
        for p in legend_percentages if p > 0
    ]

    
    
    # Calculate the largest gene node size
    max_gene_size = max(gene_node_sizes.values()) if gene_node_sizes else gene_size_scale
    
    # Create node shape legend with just cell type and gene nodes, using appropriate sizes
    node_shape_markers = [
        plt.Line2D([0], [0], marker=node_shape_cell_type, color='black', label=' Cell type', 
                   markerfacecolor='white', markersize=np.sqrt(600/np.pi)),
        plt.Line2D([0], [0], marker=node_shape_gene, color='black', label=' Gene', 
                   markerfacecolor='white', markersize=np.sqrt(max_gene_size/np.pi))
    ]
    
    # Place the node shape legend in the upper-left corner of ax_ns
    ax_ns.legend(handles=node_shape_markers, title="Node type", loc='upper left',
                 frameon=False, fontsize=12, title_fontsize=12)
    ax_ns.axis('off')
    
    # Place the dot size legend in the upper-left corner of ax_ds
    ax_ds.legend(handles=legend_markers, title="Expression %", loc='upper left',
                 frameon=False, fontsize=12, title_fontsize=12)
    ax_ds.axis('off')
    
    # ax_main.set_title("Radial Dendrogram of Cell Types with Top Marker Genes", fontsize=12)
    ax_main.axis('off')

        
    ### Whether to show the figure or not
    if show_figure:
        plt.show()  # Explicitly display the figure

    ### Save the figure
    if save:
        fig.savefig(save, bbox_inches='tight')  # Save the figure to file
        print("Figure saved to: ", save)
        plt.close(fig)  # Close the figure to prevent display
    elif not show_figure:
        plt.close(fig)  # Close the figure if not showing or saving
        
 
    
### packaged dotplot function in COSG
import pandas as pd
import scanpy as sc

def plotMarkerDotplot(
    adata,
    groupby,
    top_n_genes: int = 3,
    use_rep: str = 'X_pca',
    layer: str = None,
    key_cosg: str = 'cosg',
    swap_axes: bool = False,
    standard_scale: str = 'var',
    cmap: str = 'Spectral_r',
    save: str = None,
    **dotplot_kwargs
):
    """
    Generate a dot plot of top marker genes identified by COSG.

    The function computes the cell cluster ordering using a dendrogram (if `use_rep` is provided)
    or derives it from `adata.obs[groupby]`, extracts the top marker genes identified by COSG, 
    and plots a dotplot using Scanpy's `sc.pl.dotplot`.

    Parameters
    ----------
    adata
        Annotated data object that includes COSG results.
    groupby : str
        The cell group key in `adata.obs`, should match with the `groupby` parameter used in COSG.
    top_n_genes : int, optional (default: 3)
        The number of top marker genes to show for each group.
    use_rep : str, optional (default: 'X_pca')
        The cell low-dimensional representation key (e.g., PCA, UMAP) in `adata.obsm` used to compute the dendrogram.
    layer : str or None, optional
        The layer key to use for expression values in the dotplot (default: None).
    key_cosg : str, optional (default: 'cosg')
        The key in `adata.uns` where COSG results are stored.
    swap_axes : bool, optional (default: False)
        Whether to swap axes in the dot plot.
    standard_scale : str or None, optional
        Whether to standardize expression values across `'var'` (genes) or `'group'` (cell groups or clusters).
        Can be `'var'`, `'group'`, or `None` (default: `'var'`).
    cmap : str, optional (default: 'Spectral_r')
        The colormap used for the dot plot.
    save : str or None, optional
        If provided, saves the plot to a file. The filename should include an extension (e.g., `"cosg_markers.pdf"`).
    **dotplot_kwargs : dict
        Additional keyword arguments to pass to `sc.pl.dotplot`.

    Returns
    -------
    None
        Displays the dot plot.

    Raises
    ------
    ValueError
        If required COSG results or dendrogram information are missing, or if the provided `groupby`
        does not match the one stored in COSG parameters.

    Example
    -------
    >>> import scanpy as sc
    >>> import cosg  # Assuming plotDotPlot is part of the cosg package
    >>> adata = sc.datasets.pbmc68k_reduced()
    >>> # Using a specific low-dimensional representation for dendrogram computation and cell type ordering:
    >>> cosg.plotMarkerDotplot(
    ...     adata,
    ...     groupby='bulk_labels',
    ...     top_n_genes=3,
    ...     key_cosg='cosg',
    ...     use_rep='X_pca',
    ...     swap_axes=False,
    ...     standard_scale='var',
    ...     cmap='Spectral_r'
    ... )
    >>> # Deriving cell order from adata.obs when use_rep is None:
    >>> cosg.plotMarkerDotplot(
    ...     adata,
    ...     groupby='bulk_labels',
    ...     top_n_genes=3,
    ...     key_cosg='cosg',
    ...     use_rep=None,
    ...     swap_axes=False,
    ...     standard_scale='var',
    ...     cmap='Spectral_r'
    ... )
    """
    
    # Check that COSG results are available in adata.uns using the specified key.
    if key_cosg not in adata.uns or 'names' not in adata.uns[key_cosg]:
        raise ValueError(f"COSG results not found in `adata.uns['{key_cosg}']['names']`.")
    
    # Check that the provided groupby matches the one stored in COSG parameters.
    if 'params' not in adata.uns[key_cosg] or 'groupby' not in adata.uns[key_cosg]['params']:
        raise ValueError(
            f"The COSG results in `adata.uns['{key_cosg}']` do not contain a 'groupby' parameter in 'params'."
        )
    if adata.uns[key_cosg]['params']['groupby'] != groupby:
        raise ValueError(
            f"Provided groupby '{groupby}' does not match the groupby used in COSG results "
            f"('{adata.uns[key_cosg]['params']['groupby']}')."
        )

    
    # Set the dendrogram key
    dendro_key = 'dendrogram_' + groupby

    # Compute dendrogram or derive ordering based on use_rep
    if use_rep is not None:
        # Temporarily suppress scanpy verbosity
        original_verbosity = sc.settings.verbosity
        sc.settings.verbosity = 0  # Suppress messages
        try:
            sc.tl.dendrogram(adata, groupby=groupby, use_rep=use_rep)
        finally:
            sc.settings.verbosity = original_verbosity  # Restore original verbosity


        if dendro_key not in adata.uns or 'categories_ordered' not in adata.uns[dendro_key]:
            raise ValueError(
                f"Dendrogram results for groupby='{groupby}' not found in "
                f"`adata.uns['{dendro_key}']['categories_ordered']`."
            )
        ordering = adata.uns[dendro_key]['categories_ordered']
    else:
        # Derive ordering locally from adata.obs[groupby] without writing to adata.uns.
        if hasattr(adata.obs[groupby], "cat"):
            ordering = list(adata.obs[groupby].cat.categories)
        else:
            unique_values=adata.obs[groupby].unique()
            
            ### add a helper function here, if the cell clusters are "1", "2", ... , "10", "11", ...
            ### order them as "1", "2", ... , "10", "11", ..., instead of being "1", "10", "11", ..., "2", ...
            def _is_all_numeric(groups):
                try:
                    [float(x) for x in groups]
                    return True
                except ValueError:
                    return False

            if _is_all_numeric(unique_values):
                ordering = sorted(unique_values, key=lambda x: float(x))
            else:
                ordering = sorted(unique_values)
            
        
    # Extract the top_n_genes marker genes for each group from the COSG results.
    df_tmp = pd.DataFrame(adata.uns[key_cosg]['names'][:top_n_genes,]).T

    # Reorder rows based on the derived ordering.
    df_tmp = df_tmp.reindex(ordering)

    # Convert the DataFrame rows to a dictionary of marker genes per group.
    marker_genes_list = {idx: list(row.values) for idx, row in df_tmp.iterrows()}
    marker_genes_list = {k: v for k, v in marker_genes_list.items() if not any(isinstance(x, float) for x in v)}

    # Enable dendrogram only if use_rep is provided
    use_dendrogram = use_rep is not None  
    # Generate and display the dot plot with the provided parameters.
    sc.pl.dotplot(
        adata,
        marker_genes_list,
        groupby=groupby,
        layer=layer,
        dendrogram=use_dendrogram,
        swap_axes=swap_axes,
        standard_scale=standard_scale,
        cmap=cmap,
        save=save,
        **dotplot_kwargs
    )