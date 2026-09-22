import secrets


def password_generator(length: int, numbers: bool, lower_case: bool, upper_case: bool, special_chars: bool) -> str:
    """
    Generate a random password of a given length, ensuring to include (if True) a random (number and position) numbers,
    special characters, lower_case, upper_case and special characters.
    :param length:
    :param numbers:
    :param lower_case:
    :param upper_case:
    :param special_chars:
    :return:
    """
    # Define character sets
    digits_set = '0123456789'
    lower_set = "abcdefghijklmnopqrstuvwxyz"
    upper_set = lower_set.upper()
    special_set = "àáäâèéëêìíïîòóöôùúüûºª!\"·$%&/()=?¿'¡@[]{}-_<>"

    pools = []

    if numbers:
        pools.append(digits_set)
    if lower_case:
        pools.append(lower_set)
    if upper_case:
        pools.append(upper_set)
    if special_chars:
        pools.append(special_set)

    # If no character types are selected, return an empty string
    if not pools:
        return ""

    if length < len(pools):
        raise ValueError(f"Length must be at least {len(pools)} to accommodate all requested character types.")

    password_chars = []

    # Guarantee at least one character from each selected pool
    for pool in pools:
        password_chars.append(secrets.choice(pool))

    # Fill the remaining length with random choices from all selected pools combined
    combined_pool = "".join(pools)
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(combined_pool))

    # Cryptographically secure shuffle to randomize character positions
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)