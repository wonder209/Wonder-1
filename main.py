import flet as ft
import yt_dlp
import os
import threading

def main(page: ft.Page):
    # App Settings
    page.title = "WONDER DOWNLOADER V17"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050510"
    page.window_width = 400
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI Components
    title = ft.Text("WONDER DOWNLOADER", size=28, weight="bold", color="#00f2ea")
    sub_title = ft.Text("MASTERMIND STANDALONE", size=10, color="#ff0050", letter_spacing=4)
    
    url_input = ft.TextField(
        label="Paste Link Here",
        border_color="#00f2ea",
        border_radius=15,
        width=350,
        text_size=14,
    )

    progress_ring = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
    status_text = ft.Text("Ready", size=12, color="grey")
    
    # Progress Bar
    pb = ft.ProgressBar(width=350, color="#00f2ea", bgcolor="#1a1a3a", value=0, visible=False)

    def on_progress(d):
        if d['status'] == 'downloading':
            try:
                # Update progress bar value (0.0 to 1.0)
                p = d.get('_percent_str', '0%').replace('%','').strip()
                pb.value = float(p) / 100
                status_text.value = f"Downloading: {p}%"
                page.update()
            except:
                pass

    def start_download(e):
        if not url_input.value:
            status_text.value = "Error: Please paste a link!"
            status_text.color = "red"
            page.update()
            return

        # UI Updates
        download_btn.disabled = True
        progress_ring.visible = True
        pb.visible = True
        pb.value = 0
        status_text.value = "Initializing..."
        status_text.color = "#00ff7f"
        page.update()

        def run_dl():
            try:
                # Set path to the phone's public Download folder
                download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'
                
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': download_path,
                    'progress_hooks': [on_progress],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input.value])

                status_text.value = "Success! Saved to Downloads."
                status_text.color = "#00ff7f"
            except Exception as err:
                status_text.value = f"Error: Failed to save file."
                status_text.color = "red"
            
            download_btn.disabled = False
            progress_ring.visible = False
            page.update()

        # Run in a separate thread so the UI doesn't freeze
        threading.Thread(target=run_dl, daemon=True).start()

    download_btn = ft.ElevatedButton(
        content=ft.Row(
            [ft.Text("DOWNLOAD VIDEO", weight="bold"), progress_ring],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=350,
        height=50,
        bgcolor="#ff0050",
        color="white",
        on_click=start_download,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))
    )

    # Building the Screen
    page.add(
        title,
        sub_title,
        ft.Divider(height=20, color="transparent"),
        url_input,
        ft.Divider(height=10, color="transparent"),
        pb,
        status_text,
        ft.Divider(height=20, color="transparent"),
        download_btn,
    )

# Run the app
if __name__ == "__main__":
    ft.app(target=main)
