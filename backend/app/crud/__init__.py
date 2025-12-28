from app.crud.user import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    update_user,
    delete_user,
    authenticate_user,
    hash_password,
    verify_password,
)

from app.crud.product import (
    create_product,
    get_product_by_id,
    get_product_by_sku,
    get_all_products,
    get_products_by_category,
    search_products,
    update_product,
    delete_product,
    hard_delete_product,
    update_stock,
    is_in_stock,
)

from app.crud.category import (
    create_category,
    get_category_by_id,
    get_category_by_name,
    get_all_categories,
    update_category,
    delete_category,
    get_category_with_products_count,
)

from app.crud.cart import (
    create_cart,
    get_cart_by_id,
    get_cart_by_user_id,
    get_or_create_cart,
    get_cart_with_items,
    get_cart_summary,
    clear_cart,
    delete_cart,
)

from app.crud.cart_item import (
    add_item_to_cart,
    get_cart_item_by_id,
    get_cart_item_by_product,
    get_cart_items,
    update_cart_item,
    update_cart_item_by_product,
    remove_cart_item,
    remove_cart_item_by_product,
    increase_quantity,
    decrease_quantity,
)

from app.crud.order import (
    create_order_from_cart,
    get_order_by_id,
    get_order_by_id_and_user,
    get_user_orders,
    get_all_orders,
    get_orders_by_status,
    update_order_status,
    cancel_order,
    get_order_with_items,
    get_order_summary,
    delete_order,
)

from app.crud.order_item import (
    create_order_item,
    get_order_item_by_id,
    get_order_items,
    get_order_item_with_product,
    get_order_items_with_products,
    calculate_order_total,
)

__all__ = [
    # User
    "create_user",
    "get_user_by_id",
    "get_user_by_email",
    "get_all_users",
    "update_user",
    "delete_user",
    "authenticate_user",
    "hash_password",
    "verify_password",
    # Product
    "create_product",
    "get_product_by_id",
    "get_product_by_sku",
    "get_all_products",
    "get_products_by_category",
    "search_products",
    "update_product",
    "delete_product",
    "hard_delete_product",
    "update_stock",
    "is_in_stock",
    # Category
    "create_category",
    "get_category_by_id",
    "get_category_by_name",
    "get_all_categories",
    "update_category",
    "delete_category",
    "get_category_with_products_count",
    # Cart
    "create_cart",
    "get_cart_by_id",
    "get_cart_by_user_id",
    "get_or_create_cart",
    "get_cart_with_items",
    "get_cart_summary",
    "clear_cart",
    "delete_cart",
    # CartItem
    "add_item_to_cart",
    "get_cart_item_by_id",
    "get_cart_item_by_product",
    "get_cart_items",
    "update_cart_item",
    "update_cart_item_by_product",
    "remove_cart_item",
    "remove_cart_item_by_product",
    "increase_quantity",
    "decrease_quantity",
    # Order
    "create_order_from_cart",
    "get_order_by_id",
    "get_order_by_id_and_user",
    "get_user_orders",
    "get_all_orders",
    "get_orders_by_status",
    "update_order_status",
    "cancel_order",
    "get_order_with_items",
    "get_order_summary",
    "delete_order",
    # OrderItem
    "create_order_item",
    "get_order_item_by_id",
    "get_order_items",
    "get_order_item_with_product",
    "get_order_items_with_products",
    "calculate_order_total",
]