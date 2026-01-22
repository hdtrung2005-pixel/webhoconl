# app/context_processors.py
def cart_count(request):
    # Lấy giỏ hàng từ session (nếu chưa có thì là rỗng)
    cart = request.session.get('cart', {})
    
    # Tính tổng số lượng sản phẩm (cộng dồn các value trong dict)
    count = sum(cart.values())
    
    # Trả về biến 'cart_count' để dùng ở mọi file HTML
    return {'cart_count': count}