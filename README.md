# PetPuja — Python/Kivy Android starter

## Included
- `main.py`: Python + Kivy demo app with food list, search, cart, and demo checkout.
- `buildozer.spec`: Buildozer Android build configuration.
- `.github/workflows/build-apk.yml`: GitHub Actions workflow to build a debug APK and upload it as an artifact.

## Build APK using GitHub Actions (phone-friendly)
1. Extract this ZIP on your phone or computer.
2. Upload the **contents** to the root of your existing GitHub repository (keep the `.github/workflows/build-apk.yml` path).
3. Commit to the `main` branch, or open **Actions → Build PetPuja Android APK → Run workflow**.
4. When it succeeds, open the run and download the `PetPuja-debug-APK` artifact.

## Important
This is a starter prototype, not a production delivery platform. It does not yet have real OTP verification, address storage, server/database, restaurant owner registration/approval, admin/assistant accounts, WhatsApp notifications, live delivery tracking, or payment integration. Those require a backend and secure configuration before real customers can place orders.
