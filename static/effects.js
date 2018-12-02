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

    if (child.innerHTML == "+")
        child.innerHTML = "-"
    else
        child.innerHTML = "+"
}

function collapseItems() {
    items = localStorage.getItem("collapsed");

    if (items != null) {
        items = items.split(";");
        items_checked = {};
        cleaned_items = "";

        for (var i = 0; i < items.length; ++i) {
            if (items[i] != "" && !items_checked[items[i]]) {
                element = document.getElementById(items[i]);

                if (element !== null) {
                    collapse(element);

                    toggler = document.getElementById(element.getAttribute("id") + "-toggler");
                    if (toggler != null)
                        toggler.innerHTML = "+";
                }

                items_checked[items[i]] = true;
                cleaned_items += items[i] + ";";
            }
        }

        localStorage.setItem("collapsed", cleaned_items);
    }
}

function highlightPageJumps() {
    if (window.location.hash.length) {
        place = document.getElementById(window.location.hash.slice(1));
        if (place !== null) {
            if (performance.navigation.type != 1) {
                place.classList.add("targeted");
                window.scrollBy(0, -48);
            }
        }
    }
}
