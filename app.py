from flask import Flask, render_template, request
from stack import Stack

app = Flask(__name__)

linked_list = []
stack = Stack()

def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack_ops = []
    output = []
    
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char.isalnum():
            operand = ""
            while i < len(expression) and (expression[i].isalnum() or expression[i] == '.'):
                operand += expression[i]
                i += 1
            output.append(operand)
            continue
        elif char == '(':
            stack_ops.append(char)
        elif char == ')':
            while stack_ops and stack_ops[-1] != '(':
                output.append(stack_ops.pop())
            if stack_ops and stack_ops[-1] == '(':
                stack_ops.pop()
        elif char in precedence:
            while (stack_ops and stack_ops[-1] != '(' and 
                   stack_ops[-1] in precedence and 
                   precedence[stack_ops[-1]] >= precedence[char]):
                output.append(stack_ops.pop())
            stack_ops.append(char)
        i += 1
        
    while stack_ops:
        output.append(stack_ops.pop())
        
    return " ".join(output)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/contacts")
def contact():
    return render_template("contacts.html")


@app.route("/uppercase", methods=["GET", "POST"])
def uppercase():
    result = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        result = text.upper()
    return render_template("touppercase.html", result=result)


@app.route("/circle", methods=["GET", "POST"])
def circle():
    result = ""
    if request.method == "POST":
        radius = float(request.form.get("radius", 0))
        if radius >= 0:
            result = 3.14 * radius * radius
    return render_template("circle.html", result=result)


@app.route("/triangle", methods=["GET", "POST"])
def triangle():
    result = ""
    if request.method == "POST":
        base = float(request.form.get("base", 0))
        height = float(request.form.get("height", 0))
        if base >= 0 and height >= 0:
            result = 0.5 * base * height
    return render_template("triangle.html", result=result)


@app.route("/stack", methods=["GET", "POST"])
def stack_page():
    message = ""
    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "push":
            if value:
                stack.push(value)
                message = value + " was pushed onto the stack."
            else:
                message = "Enter a value before pushing."
        elif action == "pop":
            popped = stack.pop()
            message = "Popped: " + str(popped) if popped is not None else "The stack is empty. Nothing to pop."
        elif action == "peek":
            top_value = stack.peek()
            message = "Top element: " + str(top_value) if top_value is not None else "The stack is empty. Nothing to peek at."
        elif action == "clear":
            while stack.pop() is not None:
                pass
            message = "The stack has been cleared."

    stack_items = []
    current = stack.top
    while current:
        stack_items.append(current.data)
        current = current.next

    return render_template("stack.html", stack_items=stack_items, message=message)


@app.route("/sorting", methods=["GET", "POST"])
def sorting_page():
    message = ""
    sorted_items = []
    input_str = ""
    if request.method == "POST":
        input_str = request.form.get("numbers", "").strip()
        algo = request.form.get("algorithm", "bubble")
        try:
            arr = [float(x.strip()) if '.' in x else int(x.strip()) for x in input_str.split(",") if x.strip()]
            if not arr:
                message = "Please enter valid numbers."
            else:
                if algo == "bubble":
                    n = len(arr)
                    for i in range(n):
                        for j in range(0, n - i - 1):
                            if arr[j] > arr[j + 1]:
                                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    message = "Sorted successfully using Bubble Sort."
                elif algo == "selection":
                    n = len(arr)
                    for i in range(n):
                        min_idx = i
                        for j in range(i + 1, n):
                            if arr[j] < arr[min_idx]:
                                min_idx = j
                        arr[i], arr[min_idx] = arr[min_idx], arr[i]
                    message = "Sorted successfully using Selection Sort."
                elif algo == "insertion":
                    for i in range(1, len(arr)):
                        key = arr[i]
                        j = i - 1
                        while j >= 0 and key < arr[j]:
                            arr[j + 1] = arr[j]
                            j -= 1
                        arr[j + 1] = key
                    message = "Sorted successfully using Insertion Sort."
                
                sorted_items = [int(x) if isinstance(x, float) and x.is_integer() else x for x in arr]
        except ValueError:
            message = "Invalid format. Ensure numbers are separated by commas."

    return render_template("sorting.html", sorted_items=sorted_items, input_str=input_str, message=message)


@app.route("/infix-postfix", methods=["GET", "POST"])
def infix_postfix_page():
    result = ""
    if request.method == "POST":
        expr = request.form.get("expression", "").strip()
        if expr:
            try:
                result = infix_to_postfix(expr)
            except Exception:
                result = "Invalid expression format."
    return render_template("infix.html", result=result)


@app.route("/linked-list", methods=["GET", "POST"])
def linkedlist():
    message = ""
    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "add":
            linked_list.append(value)
            message = value + " was added to the linked list."
        elif action == "delete":
            if value in linked_list:
                linked_list.remove(value)
                message = value + " was deleted from the linked list."
            else:
                message = value + " was not found."
        elif action == "search":
            if value in linked_list:
                message = value + " was found in the linked list."
            else:
                message = value + " was not found."

    return render_template("linkedlist.html", linked_list=linked_list, message=message)


if __name__ == "__main__":
    app.run(debug=True)