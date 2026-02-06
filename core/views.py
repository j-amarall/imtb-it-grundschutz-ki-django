from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from core.services.langdock import call_langdock_assistant
from core.utils.response_splitter import split_reasoning_answer_hint


@login_required
@require_http_methods(["GET", "POST"])
def chat(request):
    user_input = ""
    reasoning = ""
    answer = ""
    hint = ""

    if request.method == "POST":
        user_input = (request.POST.get("user_input") or "").strip()
        if user_input:
            raw = call_langdock_assistant([{"role": "user", "content": user_input}])
            if raw:
                reasoning, answer, hint = split_reasoning_answer_hint(raw)

    return render(
        request,
        "core/chat.html",
        {
            "user_input": user_input,
            "reasoning": reasoning,
            "answer": answer,
            "hint": hint,
        },
    )


@login_required
def home(request):
    return redirect("chat")


def impressum(request):
    return render(request, "core/impressum.html")


def datenschutz(request):
    return render(request, "core/datenschutz.html")
