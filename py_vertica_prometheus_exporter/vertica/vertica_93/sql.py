class SQL:
    node_states = """
        select  node_id,
                node_name,
                node_state
        from    nodes;
    """

    disk_usage = """
        select  node_name,
                storage_usage,
                disk_space_used_mb,
                disk_space_free_mb,
                disk_space_free_percent
        from    disk_storage;
    """

    delete_vectors_count = """
        select  node_name,
                count(*)
        from    delete_vectors
        group by
                node_name;
    """
