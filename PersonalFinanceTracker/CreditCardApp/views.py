from django.shortcuts import render, redirect, get_object_or_404
from .models import CreditCard, UserCardApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# @login_required
# def credit_card_list(request):
#     cards = CreditCard.objects.all()
#     try:
#         user_application = UserCardApplication.objects.get(user=request.user)
#     except UserCardApplication.DoesNotExist:
#         user_application = None
#     return render(request, 'credit_cards.html', {
#         'cards': cards,
#         'user_application': user_application
#     })

# @login_required
# def apply_card(request, card_id):
#     card = get_object_or_404(CreditCard, id=card_id)
#     if UserCardApplication.objects.filter(user=request.user).exists():
#         messages.warning(request, "You have already applied for a credit card.")
#     else:
#         UserCardApplication.objects.create(user=request.user, credit_card=card)
#         messages.success(request, "Card applied successfully!")
#     return redirect('credit')

@login_required
def credit_view(request):
    cards = CreditCard.objects.all()
    return render(request ,'credit_cards.html',context={'cards': cards})


def apply_card(request, card_id):
    card = get_object_or_404(CreditCard, id=card_id)
    if UserCardApplication.objects.filter(user=request.user).exists():
        messages.warning(request, "You have already applied for a credit card.")
        return redirect('home')
    else:
        UserCardApplication.objects.create(user=request.user, credit_card=card)
        messages.success(request, "Card applied successfully!")
    return redirect('home')