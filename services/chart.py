import matplotlib.pyplot as plt


def generate_study_chart(plan: list, user_id: int) -> str:
    filename = f"chart_{user_id}.png"
    days = list(range(1, len(plan) + 1))
    plt.figure(figsize=(10, 5))
    plt.plot(days, [1] * len(plan), marker='o')
    plt.title("Учебный план")
    plt.xlabel("День")
    plt.ylabel("Задание")
    plt.xticks(days)
    plt.grid(True)
    plt.savefig(filename)
    return filename
