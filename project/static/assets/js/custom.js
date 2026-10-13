function addProductToOrder(productId) {
    const productCount = $('#product_count').val() || 1;

    $.get('/add-to-order/?product_id=' + productId + '&count=' + productCount)
        .done(function (res) {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: 'اعلان',
                    text: res.text,
                    icon: res.icon,
                    showCancelButton: false,
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: res.confirm_button_text
                }).then((result) => {
                    if (result.isConfirmed && res.status === 'not_logged_in') {
                        window.location.href = '/accounts/login/';
                    }
                });
            } else {
                alert(res.text);
                if (res.status === 'not_logged_in') {
                    window.location.href = '/accounts/login/';
                }
            }
        })
        .fail(function (jqXHR) {
            console.error('خطا در افزودن به سبد خرید:', jqXHR.status, jqXHR.responseText);
            alert('مشکلی در افزودن به سبد خرید پیش آمد. کنسول مرورگر (F12) را برای جزئیات چک کنید.');
        });
}

function removeOrderDetail(detailId) {
    $.get('/user-panel/remove-order-detail?detail_id=' + detailId).done(function (res) {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    }).fail(function (jqXHR) {
        console.error('خطا در حذف آیتم:', jqXHR.status, jqXHR.responseText);
    });
}

function changeOrderDetailCount(detailId, state) {
    $.get('/user-panel/change-order-detail?detail_id=' + detailId + '&state=' + state).done(function (res) {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    }).fail(function (jqXHR) {
        console.error('خطا در تغییر تعداد:', jqXHR.status, jqXHR.responseText);
    });
}
