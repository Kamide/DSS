function storeCollapsedItem(id) {
    items = localStorage.getItem("collapsed")
    if (items == null)
        localStorage.setItem("collapsed", id + ";");
    else
        localStorage.setItem("collapsed", localStorage.getItem("collapsed") + id + ";");
}

function discardCollapsedItem(id) {
    items = localStorage.getItem("collapsed")
    if (items != null)
        localStorage.setItem("collapsed", localStorage.getItem("collapsed").replace(id + ";", ""));
}

function expand(element) {
    element.collapsed = false;
    element.classList.remove("collapsed");
}

function collapse(element) {
    element.collapsed = true;
    element.classList.add("collapsed");
}

function expandCollapseParentOf(child) {
    parent = child.parentElement;

    if (!parent.collapsed) {
        collapse(parent);
        storeCollapsedItem(parent.getAttribute("id"));
    }
    else {
        expand(parent);
        discardCollapsedItem(parent.getAttribute("id"));
    }

    switch(child.innerHTML) {
        case "-":
            child.innerHTML = "+";
            break;
        case "+":
            child.innerHTML = "-";
            break;
    }
}

function display() {
    items = localStorage.getItem("collapsed");
    cleaned_items = "";
    if (items != null) {
        items = items.split(";");
        for (var i = items.length - 1; i >= 0; --i) {
            if (items[i] != "") {
                element = document.getElementById(items[0]);
                if (element !== null) {
                    collapse(element);
                    element.getElementsByClassName("toggler")[0].innerHTML = "+";
                    cleaned_items += items[i] + ";";
                }
            }
        }
    }
    localStorage.setItem("collapsed", cleaned_items);
}
