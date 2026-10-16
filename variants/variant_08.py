VARIANT = 23

def script():
    return """
    WITH moved AS (
        DELETE FROM purchase 
        WHERE shipped_on < '2025-05-01' 
        RETURNING *
    )
    INSERT INTO purchase_archive (id, customer_id, product_id, quantity, ordered_on, shipped_on)
    SELECT id, customer_id, product_id, quantity, ordered_on, shipped_on 
    FROM moved;

    WITH new_customer AS (
        INSERT INTO customer (full_name, email) 
        VALUES ('Назар Кулик', 'nazar.k@example.com') 
        RETURNING id
    )
    INSERT INTO purchase (customer_id, product_id, quantity, ordered_on)
    SELECT id, (SELECT id FROM product WHERE sku = 'SKU-0007'), 3, '2025-09-01'
    FROM new_customer;
    """