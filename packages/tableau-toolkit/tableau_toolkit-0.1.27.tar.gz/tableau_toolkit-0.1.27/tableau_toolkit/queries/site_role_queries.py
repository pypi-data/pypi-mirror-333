from psycopg2 import sql


def get_site_roles_query():
    return sql.SQL(
        """
        with
        user_rank as (
        select 
        u.id user_id,
        u.site_id site_id,
        sr.id site_role_id,
        row_number() over(partition by su.name order by sr.licensing_rank desc) rnk
        from users u
        join system_users su
        on su.id = u.system_user_id
        join site_roles sr
        on sr.id = u.site_role_id
        where su.admin_level <> 10
        ),
        server_admins as (
        select 
        'Server Administrator' object_name,
        count(distinct su.name) unique_user_cnt
        from system_users su
        where su.admin_level = 10
        ),
        final as (
        select
        sr.display_name object_name,
        count(distinct su.name) unique_user_cnt
        from users u
        join system_users su
        on su.id = u.system_user_id
        join user_rank ur
        on ur.user_id = u.id
        and ur.site_id = u.site_id
        join site_roles sr
        on sr.id = u.site_role_id
        where ur.rnk = 1
        group by 1
        union all
        select 
        object_name,
        unique_user_cnt
        from server_admins
        union all
        select
        'Any site role' object_name,
        count(distinct su.name) unique_user_cnt
        from system_users su
        join users u
          on u.system_user_id = su.id
        join site_roles sr
          on sr.id = u.site_role_id
        )
        select * from final
        ORDER BY
            CASE
                WHEN {sort_column} IS NULL THEN 1
                ELSE 0
            END,
            {sort_column} {sort_direction}
        LIMIT %(limit)s
    """
    )
