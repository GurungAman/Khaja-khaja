## how checkout in this system works

- user creates order item/ adds to cart. Initialy, orderd boolean field set to false to denote that order has not yet been  made. The item is placed in the cart.
- User checks out, then order is created from all the order items/cart items whose ordered field is set as false.
- After user pays for items, order status is set changed 'order created' from Null.
- Notification for orderitem is sent to their corresponding restaurant.

- user adds item to cart  -> order item created -> Place order -> order created with all order items -> checkout ->  notify respective restaurants  -> deliver orders

## Tings To do;
 - payment Integration