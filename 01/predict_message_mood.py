from some_model import SomeModel


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:

    if not isinstance(message, str):
        raise TypeError(
            f"Expected a string, got: {type(message).__name__}"
        )

    if not isinstance(bad_thresholds, float):
        raise TypeError(
            f"Expected a float, got: {type(bad_thresholds).__name__}"
        )

    if not isinstance(good_thresholds, float):
        raise TypeError(
            f"Expected a float, got: {type(good_thresholds).__name__}"
        )

    model = SomeModel()
    prediction = model.predict(message)

    if prediction < bad_thresholds:
        return "неуд"

    if prediction > good_thresholds:
        return "отл"

    return "норм"
