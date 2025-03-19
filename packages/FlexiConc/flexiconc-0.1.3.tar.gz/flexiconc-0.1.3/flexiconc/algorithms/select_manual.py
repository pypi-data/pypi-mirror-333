def select_manual(conc, **args):
    """
    Manually selects lines into a subset by providing a list of line IDs or by specifying groups
    (by labels or numbers) from the active node's grouping result. Groups may be partitions or clusters.
    In case of clusters (which may be nested), the entire grouping structure is traversed recursively
    to collect all groups that match the given identifiers.

    Args:
        conc (Union[Concordance, ConcordanceSubset]): The concordance or its subset.
        args (dict): Arguments include:
            - line_ids (list, optional): A list of specific line IDs to include in the subset.
            - groups (list, optional): A list of group identifiers (either integers or strings) that
              refer to groups (partitions or clusters) in the grouping_result.
            - active_node (object, optional): The active node containing the grouping_result.

    Returns:
        dict: A dictionary containing:
            - "selected_lines": A sorted list of unique selected line IDs.
            - "line_count": The total number of selected lines.
    """

    # Metadata for the algorithm
    select_manual._algorithm_metadata = {
        "name": "Manual Line Selection",
        "description": (
            "Manually selects lines into a subset by specifying line IDs or groups (partitions or clusters) "
            "from the active node's grouping result."
        ),
        "algorithm_type": "selection",
        "args_schema": {
            "type": "object",
            "properties": {
                "line_ids": {
                    "type": ["array"],
                    "items": {"type": "integer"},
                    "description": "A list of specific line IDs to include in the subset.",
                },
                "groups": {
                    "type": ["array"],
                    "items": {"type": ["string", "integer"]},
                    "description": (
                        "A list of group identifiers (by label or number) to include lines from. "
                        "For clusters, groups may be nested, and all matching groups in the hierarchy will be used."
                    ),
                },
                "active_node": {
                    "description": "The active node containing the grouping_result.",
                }
            },
            "required": []
        }
    }

    selected_line_ids = set()

    # Extract arguments
    line_ids = args.get("line_ids", None)
    active_node = args.get("active_node", None)
    groups = args.get("groups", None)

    # Add explicitly specified line_ids.
    if line_ids:
        selected_line_ids.update(line_ids)

    if groups and active_node and hasattr(active_node, "grouping_result"):
        grouping_result = active_node.grouping_result
        # Determine whether the grouping_result contains partitions or clusters.
        if isinstance(grouping_result, dict):
            if "partitions" in grouping_result:
                parent_groups = grouping_result["partitions"]
            elif "clusters" in grouping_result:
                parent_groups = grouping_result["clusters"]
            else:
                parent_groups = []
        else:
            parent_groups = []

        # For clusters, recursively flatten them.
        def flatten_groups(groups_list):
            flat = []
            for group in groups_list:
                flat.append(group)
                if "children" in group and group["children"]:
                    flat.extend(flatten_groups(group["children"]))
            return flat

        flat_groups = flatten_groups(parent_groups)

        # Process each group identifier.
        for group_identifier in groups:
            if isinstance(group_identifier, int):
                # Match by group id
                matching_groups = [g for g in flat_groups if g.get("id") == group_identifier]
                for group in matching_groups:
                    selected_line_ids.update(group.get("line_ids", []))
            elif isinstance(group_identifier, str):
                # Match by group label
                matching_groups = [g for g in flat_groups if g.get("label") == group_identifier]
                for group in matching_groups:
                    selected_line_ids.update(group.get("line_ids", []))

    # Sort the selected line IDs and convert to list.
    selected_line_ids = sorted(selected_line_ids)
    return {"selected_lines": selected_line_ids}
