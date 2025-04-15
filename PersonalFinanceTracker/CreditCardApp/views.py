from django.shortcuts import render, redirect, get_object_or_404
from .models import CreditCard, UserCardApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreditCardForm


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
def all_credit_users_view(request):
    cards = UserCardApplication.objects.all()
    return render(request ,'allcards.html',context={'cards': cards})




@login_required
def delete_user_view(request, card_id):
    user_card = UserCardApplication.objects.get(id=card_id)
    
    user_card.delete()
    messages.success(request, 'User Credit Card deleted successfully!')
   
    return redirect('home')


#----------------–––––––––––––––––––––––––––––––––––––––--------------------------------------------------------------

# @login_required
# def update_credit_view(request, card_id):
#     user_card = UserCardApplication.objects.get(id=card_id)
#     if request.method == 'POST':
#         user_card.credit_card = request.POST.get('credit_card')

#         user_card.save()
#         messages.success(request, "Profile updated successfully!")
#         return redirect('profile')
    


@login_required
def update_credit_view(request, card_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superusers only.")
        return redirect('home')

    try:
        user_card = UserCardApplication.objects.get(id=card_id)
    except UserCardApplication.DoesNotExist:
        messages.error(request, "Application not found.")
        return redirect('allcards')

    available_cards = CreditCard.objects.all()

    if request.method == 'POST':
        selected_card_id = request.POST.get('credit_card')
        try:
            selected_card = CreditCard.objects.get(id=selected_card_id)
            user_card.credit_card = selected_card
            user_card.save()
            messages.success(request, "Credit card updated successfully!")
        except CreditCard.DoesNotExist:
            messages.error(request, "Selected credit card does not exist.")
        
        return redirect('allcards')

    return render(request, 'update_credit.html', {
        'user_card': user_card,
        'available_cards': available_cards
    })


#----------------–––––––––––––––––––––––––––––––––––––––--------------------------------------------------------------

