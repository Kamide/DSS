from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(request, queryset, default_count=10):
    count = request.GET.get('count')

    if count is None:
        count = default_count
    else:
        try:
            count = max(1, int(count))
        except ValueError:
            count = default_count

    paginator = Paginator(queryset, count)
    page = request.GET.get('page')

    if page is None:
        page = 1
    else:
        try:
            page = max(0, int(page))
            if page > paginator.num_pages:
                page = paginator.num_pages
        except ValueError:
            page = 1

    queryset = paginator.get_page(page)

    # Get 5 numbers before and after the current page number
    # Ignore numbers that render invalid page numbers
    sequence = []
    for i in range(max(page-5, 1), min(page+5, paginator.num_pages) + 1):
        sequence.append(i)

    return queryset, count, sequence
