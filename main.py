import flet as ft
import yt_dlp
import os
import threading

def main(page: ft.Page):
    page.title = "WONDER DOWNLOADER"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050510"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text("WONDER DOWNLOADER", size=28, weight="bold", color="#00f2ea")
    url_input = ft.TextField(label="Paste Link Here", border_color="#00f2ea", width=350)
    status_text = ft.Text("Ready", color="grey")

    def run_dl(video_url):
        try:
            # Saving to the app's internal folder to avoid permission errors
            ydl_opts = {'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            status_text.value = "Success! Video Downloaded."
            status_text.color = "green"
        except Exception:
            status_text.value = "Error: Download Failed."
            status_text.color = "red"
        page.update()

    def start_download(e):
        if not url_input.value:
            status_text.value = "Please paste a link!"
            page.update()
            return
        status_text.value = "Downloading..."
        page.update()
        threading.Thread(target=run_dl, args=(url_input.value,), daemon=True).start()

    page.add(
        title,
        ft.Divider(height=20, color="transparent"),
        url_input,
        status_text,
        ft.ElevatedButton("DOWNLOAD", on_click=start_download, bgcolor="#ff0050", color="white")
    )

if __name__ == "__main__":
    ft.app(target=main)
