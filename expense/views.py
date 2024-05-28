from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.http import JsonResponse

# Create your views here.

def expense_list(request, trip_id):
    expenses = Expense.objects.filter(trip_id=trip_id).order_by('date')
    total_amount = sum(expense.amount for expense in expenses if expense.category == 'expense')
    remaining_balance = 10000 - total_amount  # Assuming an initial balance of 10000 for the trip
    return render(request, 'expense/expense_list.html', {
        'expenses': expenses,
        'total_amount': total_amount,
        'remaining_balance': remaining_balance,
    })

def add_expense(request, trip_id):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.trip_id = trip_id
            expense.save()
            return redirect('expense_list', trip_id=trip_id)
    else:
        form = ExpenseForm()
    return render(request, 'expense/add_expense.html', {'form': form})

def edit_expense(request, trip_id, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list', trip_id=trip_id)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/edit_expense.html', {'form': form})

def delete_expense(request, trip_id, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('expense_list', trip_id=trip_id)

def send_to_trips_detail(request, trip_id):
    expenses = Expense.objects.filter(trip_id=trip_id).order_by('date')
    data = [
        {
            'description': expense.description,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date,
        }
        for expense in expenses
    ]
    # Assuming there's a view in trips app that handles this data
    return JsonResponse({'trip_id': trip_id, 'expenses': data})