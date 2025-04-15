from django.shortcuts import render, redirect, get_object_or_404
from .models import CreditCard, UserCardApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreditCardForm

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
def add_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('credit')
    else:
        form = CreditCardForm()
    return render(request, 'add_card.html', context={'form': form})


@login_required
def credit_view(request):
    cards = CreditCard.objects.all()
    return render(request ,'credit_cards.html',context={'cards': cards})

@login_required
def apply_card(request, card_id):
    card = get_object_or_404(CreditCard, id=card_id)
    if UserCardApplication.objects.filter(user=request.user).exists():
        messages.warning(request, "You have already applied for a credit card.")
        return redirect('home')
    else:
        UserCardApplication.objects.create(user=request.user, credit_card=card)
        messages.success(request, "Card applied successfully!")
    return redirect('home')


@login_required
def delete_user_view(request, card_id):
    user_card = UserCardApplication.objects.get(id=card_id)
    
    user_card.delete()
    messages.success(request, 'User Credit Card deleted successfully!')
   
    return redirect('home')


@login_required
def all_credit_users_view(request):
    cards = UserCardApplication.objects.all()
    return render(request ,'allcards.html',context={'cards': cards})