import math
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk


def build_watermark_stamp(
    base_size: tuple[int, int],
    text: str = "",
    logo_img: Image.Image | None = None,
    scale_pct: float = 4.5,
    text_opacity: int = 160,
    text_color: tuple[int, int, int] = (0, 0, 0),
    logo_opacity: int = 255,
    logo_boost: float = 1.0,
    logo_tint: tuple[int, int, int] | None = None,
) -> Image.Image | None:
    text = text.strip()
    if not text and logo_img is None:
        return None

    min_dim = min(base_size)
    font_size = max(12, int(min_dim * (scale_pct / 100.0)))
    font = ImageFont.load_default(size=font_size)
    padding = int(font_size * 0.4)

    logo = None
    logo_w, logo_h = 0, 0
    if logo_img is not None:
        logo = logo_img.copy()
        target_h = int(font_size * 1.4)
        aspect_ratio = logo.width / max(1, logo.height)
        logo_w = max(1, int(target_h * aspect_ratio))
        logo_h = max(1, target_h)
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

        alpha = logo.getchannel("A")
        if logo_tint is not None:
            tinted = Image.new("RGBA", logo.size, (*logo_tint, 255))
            tinted.putalpha(alpha)
            logo = tinted

        scale = (logo_opacity / 255.0) * logo_boost
        alpha = alpha.point(lambda p: min(255, int(p * scale)))
        logo.putalpha(alpha)

    text_w, text_h = 0, 0
    bbox = (0, 0, 0, 0)
    if text:
        dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        bbox = dummy_draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    gap = padding if (logo is not None and text) else 0
    stamp_w = max(1, logo_w + gap + text_w)
    stamp_h = max(1, logo_h, text_h)

    stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))

    if logo is not None:
        logo_y = (stamp_h - logo_h) // 2
        stamp.paste(logo, (0, logo_y), logo)

    if text:
        draw = ImageDraw.Draw(stamp)
        text_x = logo_w + gap - bbox[0]
        text_y = (stamp_h - text_h) // 2 - bbox[1]
        draw.text((text_x, text_y), text, font=font, fill=(*text_color, text_opacity))

    return stamp


def apply_watermark(
    base_image: Image.Image,
    text: str = "",
    logo_img: Image.Image | None = None,
    scale_pct: float = 4.5,
    angle: float = 45.0,
    text_opacity: int = 160,
    text_color: tuple[int, int, int] = (0, 0, 0),
    logo_opacity: int = 255,
    logo_boost: float = 1.0,
    logo_tint: tuple[int, int, int] | None = None,
    tiled: bool = True,
    position: str = "Center",
) -> Image.Image:
    img_w, img_h = base_image.size
    stamp = build_watermark_stamp(
        (img_w, img_h),
        text=text,
        logo_img=logo_img,
        scale_pct=scale_pct,
        text_opacity=text_opacity,
        text_color=text_color,
        logo_opacity=logo_opacity,
        logo_boost=logo_boost,
        logo_tint=logo_tint,
    )

    if stamp is None:
        return base_image.copy()

    if not tiled:
        rotated_stamp = stamp.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
        overlay = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        margin = int(min(img_w, img_h) * 0.04)

        positions = {
            "Center": ((img_w - rotated_stamp.width) // 2, (img_h - rotated_stamp.height) // 2),
            "Top-Left": (margin, margin),
            "Top-Right": (img_w - rotated_stamp.width - margin, margin),
            "Bottom-Left": (margin, img_h - rotated_stamp.height - margin),
            "Bottom-Right": (
                img_w - rotated_stamp.width - margin,
                img_h - rotated_stamp.height - margin,
            ),
        }
        pos = positions.get(position, positions["Center"])
        overlay.paste(rotated_stamp, pos, rotated_stamp)
    else:
        step_x = max(10, int(stamp.width * 1.5))
        step_y = max(10, int(stamp.height * 3.0))
        diagonal = int(math.hypot(img_w, img_h))

        overlay = Image.new("RGBA", (diagonal, diagonal), (0, 0, 0, 0))
        for row_idx, y in enumerate(range(0, diagonal, step_y)):
            x_offset = (step_x // 2) if row_idx % 2 == 1 else 0
            for x in range(-step_x, diagonal + step_x, step_x):
                overlay.paste(stamp, (x + x_offset, y), stamp)

        overlay = overlay.rotate(angle, resample=Image.Resampling.BICUBIC)
        crop_left = (diagonal - img_w) // 2
        crop_top = (diagonal - img_h) // 2
        overlay = overlay.crop((crop_left, crop_top, crop_left + img_w, crop_top + img_h))

    return Image.alpha_composite(base_image, overlay)


class WatermarkApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Watermark Studio")
        self.root.geometry("1080x720")
        self.root.minsize(900, 620)

        # State
        self.full_image: Image.Image | None = None
        self.preview_base: Image.Image | None = None
        self.logo_image: Image.Image | None = None
        self.tk_preview: ImageTk.PhotoImage | None = None
        self.input_path: str = ""
        self._after_id: str | None = None

        # Variables
        self.image_label_var = tk.StringVar(value="No image selected")
        self.logo_label_var = tk.StringVar(value="No logo selected")
        self.text_var = tk.StringVar(value="Draft picture")
        self.text_color_var = tk.StringVar(value="Black")
        self.logo_tint_var = tk.StringVar(value="Original")
        self.text_opacity_var = tk.IntVar(value=160)
        self.logo_opacity_var = tk.IntVar(value=255)
        self.logo_boost_var = tk.DoubleVar(value=1.0)
        self.scale_var = tk.DoubleVar(value=4.5)
        self.angle_var = tk.DoubleVar(value=45.0)
        self.tiled_var = tk.BooleanVar(value=True)
        self.position_var = tk.StringVar(value="Center")
        self.output_filename_var = tk.StringVar(value="watermarked_image.jpg")
        self.jpeg_quality_var = tk.IntVar(value=90)

        self._build_ui()
        self._bind_traces()

    def _build_ui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Left Panel: Controls
        controls = ttk.Frame(self.root, padding=14)
        controls.grid(row=0, column=0, sticky="ns")

        # --- 1. Files ---
        file_frame = ttk.LabelFrame(controls, text="1. Files", padding=10)
        file_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(file_frame, text="Load Image...", command=self.load_image).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Label(file_frame, textvariable=self.image_label_var, width=28, foreground="#555").grid(
            row=0, column=1, padx=(8, 0), sticky="w"
        )

        logo_btn_row = ttk.Frame(file_frame)
        logo_btn_row.grid(row=1, column=0, pady=(6, 0), sticky="ew")
        ttk.Button(logo_btn_row, text="Load Logo...", command=self.load_logo).pack(side="left")
        ttk.Button(logo_btn_row, text="Clear", width=5, command=self.clear_logo).pack(
            side="left", padx=(4, 0)
        )
        ttk.Label(file_frame, textvariable=self.logo_label_var, width=28, foreground="#555").grid(
            row=1, column=1, padx=(8, 0), pady=(6, 0), sticky="w"
        )

        # --- 2. Content & Color ---
        content_frame = ttk.LabelFrame(controls, text="2. Text & Logo Style", padding=10)
        content_frame.pack(fill="x", pady=(0, 10))
        content_frame.columnconfigure(1, weight=1)

        ttk.Label(content_frame, text="Watermark Text:").grid(row=0, column=0, sticky="w")
        ttk.Entry(content_frame, textvariable=self.text_var).grid(
            row=0, column=1, sticky="ew", padx=(8, 0)
        )

        ttk.Label(content_frame, text="Text Color:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        color_row = ttk.Frame(content_frame)
        color_row.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
        ttk.Radiobutton(color_row, text="Black", value="Black", variable=self.text_color_var).pack(
            side="left"
        )
        ttk.Radiobutton(color_row, text="White", value="White", variable=self.text_color_var).pack(
            side="left", padx=(12, 0)
        )

        ttk.Label(content_frame, text="Logo Tint:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        tint_row = ttk.Frame(content_frame)
        tint_row.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
        for opt in ("Original", "Black", "White"):
            ttk.Radiobutton(tint_row, text=opt, value=opt, variable=self.logo_tint_var).pack(
                side="left", padx=(0, 10)
            )

        # --- 3. Opacity & Sizing ---
        sliders_frame = ttk.LabelFrame(controls, text="3. Opacity, Size & Rotation", padding=10)
        sliders_frame.pack(fill="x", pady=(0, 10))
        sliders_frame.columnconfigure(1, weight=1)

        self._add_slider(sliders_frame, 0, "Text Opacity:", self.text_opacity_var, 0, 255, is_int=True)
        self._add_slider(sliders_frame, 1, "Logo Opacity:", self.logo_opacity_var, 0, 255, is_int=True)
        self._add_slider(sliders_frame, 2, "Logo Boost:", self.logo_boost_var, 1.0, 4.0)
        self._add_slider(sliders_frame, 3, "Scale (%):", self.scale_var, 1.5, 15.0)
        self._add_slider(sliders_frame, 4, "Angle (°):", self.angle_var, -90.0, 90.0)

        # --- 4. Layout ---
        layout_frame = ttk.LabelFrame(controls, text="4. Layout", padding=10)
        layout_frame.pack(fill="x", pady=(0, 10))

        self.tiled_check = ttk.Checkbutton(
            layout_frame,
            text="Tile across entire image",
            variable=self.tiled_var,
            command=self._toggle_position_state,
        )
        self.tiled_check.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(layout_frame, text="Single Position:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.position_combo = ttk.Combobox(
            layout_frame,
            textvariable=self.position_var,
            values=("Center", "Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"),
            state="disabled",
            width=18,
        )
        self.position_combo.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))

        # --- 5. Export ---
        export_frame = ttk.LabelFrame(controls, text="5. Save Output", padding=10)
        export_frame.pack(fill="x")
        export_frame.columnconfigure(1, weight=1)

        ttk.Label(export_frame, text="Filename:").grid(row=0, column=0, sticky="w")
        ttk.Entry(export_frame, textvariable=self.output_filename_var).grid(
            row=0, column=1, sticky="ew", padx=(8, 0)
        )

        self._add_slider(export_frame, 1, "JPG/WebP Quality:", self.jpeg_quality_var, 50, 100, is_int=True)

        ttk.Button(export_frame, text="Save Watermarked Image", command=self.save_image).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

        # Right Panel: Live Preview
        preview_frame = ttk.LabelFrame(self.root, text="Live Preview", padding=10)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 14), pady=14)
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(preview_frame, bg="#222222", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _e: self.schedule_preview())

    def _add_slider(self, parent, row: int, label: str, var, from_: float, to: float, is_int: bool = False):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        val_label = ttk.Label(parent, width=5, anchor="e")
        val_label.grid(row=row, column=2, sticky="e", padx=(6, 0))

        def update_lbl(*_):
            val_label.config(text=f"{int(var.get())}" if is_int else f"{var.get():.1f}")

        var.trace_add("write", update_lbl)
        update_lbl()

        scale = ttk.Scale(parent, from_=from_, to=to, variable=var, orient="horizontal")
        scale.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=3)

    def _bind_traces(self):
        for var in (
            self.text_var,
            self.text_color_var,
            self.logo_tint_var,
            self.text_opacity_var,
            self.logo_opacity_var,
            self.logo_boost_var,
            self.scale_var,
            self.angle_var,
            self.tiled_var,
            self.position_var,
        ):
            var.trace_add("write", lambda *_: self.schedule_preview())

    def _toggle_position_state(self):
        self.position_combo.config(state="disabled" if self.tiled_var.get() else "readonly")

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Select Base Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            img = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not open image:\n{exc}")
            return

        self.input_path = path
        self.full_image = img
        # Create a faster downscaled copy for smooth live slider previews
        preview = img.copy()
        preview.thumbnail((1100, 1100), Image.Resampling.LANCZOS)
        self.preview_base = preview

        base_name, _ = os.path.splitext(os.path.basename(path))
        self.image_label_var.set(f"{os.path.basename(path)} ({img.width}×{img.height})")
        self.output_filename_var.set(f"{base_name}_watermarked.jpg")
        self.schedule_preview()

    def load_logo(self):
        path = filedialog.askopenfilename(
            title="Select Logo Image (PNG/WebP recommended)",
            filetypes=[("Image files", "*.png *.webp *.jpg *.jpeg *.bmp"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            self.logo_image = Image.open(path).convert("RGBA")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not open logo:\n{exc}")
            return

        self.logo_label_var.set(os.path.basename(path))
        self.schedule_preview()

    def clear_logo(self):
        self.logo_image = None
        self.logo_label_var.set("No logo selected")
        self.schedule_preview()

    def _get_params(self) -> dict:
        text_color = (0, 0, 0) if self.text_color_var.get() == "Black" else (255, 255, 255)
        tint_choice = self.logo_tint_var.get()
        logo_tint = None
        if tint_choice == "Black":
            logo_tint = (0, 0, 0)
        elif tint_choice == "White":
            logo_tint = (255, 255, 255)

        return {
            "text": self.text_var.get(),
            "logo_img": self.logo_image,
            "scale_pct": float(self.scale_var.get()),
            "angle": float(self.angle_var.get()),
            "text_opacity": int(self.text_opacity_var.get()),
            "text_color": text_color,
            "logo_opacity": int(self.logo_opacity_var.get()),
            "logo_boost": float(self.logo_boost_var.get()),
            "logo_tint": logo_tint,
            "tiled": bool(self.tiled_var.get()),
            "position": self.position_var.get(),
        }

    def schedule_preview(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(40, self.update_preview)

    def update_preview(self):
        self._after_id = None
        self.canvas.delete("all")
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())

        if self.preview_base is None:
            self.canvas.create_text(
                cw // 2,
                ch // 2,
                text="Click 'Load Image...' on the left to start",
                fill="#AAAAAA",
                font=("sans-serif", 13),
            )
            return

        rendered = apply_watermark(self.preview_base, **self._get_params())

        # Fit rendered image into canvas while preserving aspect ratio
        ratio = min(cw / rendered.width, ch / rendered.height)
        disp_w = max(1, int(rendered.width * ratio))
        disp_h = max(1, int(rendered.height * ratio))
        display_img = rendered.resize((disp_w, disp_h), Image.Resampling.LANCZOS)

        self.tk_preview = ImageTk.PhotoImage(display_img)
        self.canvas.create_image(cw // 2, ch // 2, image=self.tk_preview, anchor="center")

    def save_image(self):
        if self.full_image is None:
            messagebox.showwarning("No Image", "Please load a base image first.")
            return

        filename = self.output_filename_var.get().strip()
        if not filename:
            messagebox.showwarning("Missing Filename", "Please enter an output filename.")
            return

        # Save in the same directory as the input image unless a full path was entered
        if not os.path.dirname(filename) and self.input_path:
            out_path = os.path.join(os.path.dirname(self.input_path), filename)
        else:
            out_path = filename

        # Default to .jpg if no extension was typed
        if not os.path.splitext(out_path)[1]:
            out_path += ".jpg"

        try:
            result = apply_watermark(self.full_image, **self._get_params())
            ext = os.path.splitext(out_path)[1].lower()
            quality = int(self.jpeg_quality_var.get())

            if ext in (".jpg", ".jpeg", ".bmp"):
                result.convert("RGB").save(out_path, quality=quality)
            elif ext == ".webp":
                result.save(out_path, quality=quality)
            else:
                result.save(out_path)

            messagebox.showinfo("Saved", f"Saved watermarked image to:\n{out_path}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Failed to save image:\n{exc}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()