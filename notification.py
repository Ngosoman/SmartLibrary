from plyer import notification
import winsound  # For Windows sounds

def alert_overdue():
    notification.notify(
        title="Overdue Book!",
        message="Student X forgot to return 'Y'!",
        timeout=10
    )
    winsound.PlaySound("alert.tomorrow.mp3.mp3", winsound.SND_ASYNC)  # Your sound file