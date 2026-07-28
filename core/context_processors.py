from django.http import HttpRequest


def app_account_context(request: HttpRequest) -> dict[str, bool | str]:
    """
    Универсальный контекст для навбара:
    - определяет, есть ли у текущего приложения личный кабинет,
    - определяет, мы в личном кабинете или в публичной части,
    - отдаёт универсальные переменные для шаблона.
    """

    namespace = getattr(request.resolver_match, "namespace", "") or ""

    has_account = False
    in_account = False
    account_url_name = ""
    public_url_name = ""

    # БЛОГ
    if "blog" in namespace:
        has_account = True

        if namespace == "blog_account":
            in_account = True
            account_url_name = "blog_account:dashboard"
            public_url_name = "blog_public:post_list"

        elif namespace == "blog_public":
            in_account = False
            account_url_name = "blog_account:dashboard"
            public_url_name = "blog_public:post_list"

        else:
            raise ValueError(f"Unknown blog namespace: {namespace}")

    # КАТАЛОГ
    if "catalog" in namespace:
        # сейчас у каталога нет личного кабинета
        has_account = False

    return {
        "has_account": has_account,
        "in_account": in_account,
        "account_url_name": account_url_name,
        "public_url_name": public_url_name,
    }
