
# Linux Directory Structure (ساختار دایرکتوری لینوکس)

## 1. `/` (Root) / (ریشه)
- **English**: The root directory, the top-level directory in the filesystem. All other directories stem from here.
- **فارسی**: دایرکتوری ریشه یا همان Root که همه دایرکتوری‌های دیگر از آن منشعب می‌شوند.

## 2. `/bin`
- **English**: Contains essential binaries that are necessary for the basic functioning of the system, like `ls`, `cp`, and `mv`.
- **فارسی**: شامل فایل‌های اجرایی (باینری‌ها) است که برای کارکردهای پایه سیستم مورد نیاز هستند.

## 3. `/boot`
- **English**: Contains files necessary for booting the system, including the Linux kernel and bootloader configuration files.
- **فارسی**: شامل فایل‌های ضروری برای بوت شدن سیستم، از جمله کرنل لینوکس و فایل‌های پیکربندی بوت‌لودر.

## 4. `/dev`
- **English**: Contains device files that represent hardware devices like disks, USB ports, etc.
- **فارسی**: شامل فایل‌های دستگاه (device files) است که نمایانگر دستگاه‌های سخت‌افزاری سیستم هستند.

## 5. `/etc`
- **English**: Contains configuration files for the system, services, and applications.
- **فارسی**: شامل فایل‌های پیکربندی سیستم است. این دایرکتوری محل تنظیمات مربوط به سرویس‌ها و برنامه‌ها است.

## 6. `/home`
- **English**: Contains home directories for users. Each user has a personal folder under this directory.
- **فارسی**: شامل دایرکتوری‌های کاربران است. هر کاربر یک پوشه جداگانه در این دایرکتوری دارد.

## 7. `/lib`
- **English**: Contains shared libraries required by system programs and binaries.
- **فارسی**: شامل کتابخانه‌های اشتراکی (Shared Libraries) است که توسط برنامه‌ها و سیستم مورد استفاده قرار می‌گیرد.

## 8. `/media`
- **English**: Used for mounting external devices like USB drives and CD/DVDs. Devices are automatically mounted here.
- **فارسی**: پوشه‌ای که برای مانت کردن دستگاه‌های خارجی مثل دیسک‌های USB و CD/DVD استفاده می‌شود.

## 9. `/mnt`
- **English**: Used for manually mounting external filesystems.
- **فارسی**: به طور موقت برای مانت کردن فایل‌سیستم‌های خارجی به کار می‌رود.

## 10. `/opt`
- **English**: Contains optional software, typically third-party applications not managed by the system's package manager.
- **فارسی**: دایرکتوری اختیاری که برای نصب نرم‌افزارهای شخص ثالث (third-party) استفاده می‌شود.

## 11. `/proc`
- **English**: A virtual directory containing system and process information.
- **فارسی**: یک دایرکتوری مجازی که اطلاعات سیستم و فرآیندهای در حال اجرا را ذخیره می‌کند.

## 12. `/root`
- **English**: The home directory of the root (administrator) user.
- **فارسی**: دایرکتوری خانگی کاربر root (کاربر اصلی سیستم).

## 13. `/run`
- **English**: Contains runtime data such as process IDs and sockets.
- **فارسی**: یک دایرکتوری موقت که اطلاعات در حال اجرای سیستم را ذخیره می‌کند.

## 14. `/sbin`
- **English**: Contains system binaries used for administrative tasks, typically only executable by the root user.
- **فارسی**: شامل دستورات سیستمی و مدیریتی (System Binaries) که معمولاً فقط توسط کاربر root اجرا می‌شوند.

## 15. `/srv`
- **English**: Contains data for services provided by the system (e.g., web server files).
- **فارسی**: شامل داده‌های مربوط به سرویس‌های ارائه‌شده توسط سیستم است.

## 16. `/sys`
- **English**: Another virtual directory, focusing on hardware information.
- **فارسی**: دایرکتوری مجازی دیگری که اطلاعات سخت‌افزاری و دستگاه‌های سیستم را نشان می‌دهد.

## 17. `/tmp`
- **English**: Contains temporary files, which are usually deleted on reboot.
- **فارسی**: شامل فایل‌های موقتی است که توسط برنامه‌ها ایجاد می‌شوند.

## 18. `/usr`
- **English**: Contains user-installed software and libraries.
- **فارسی**: شامل نرم‌افزارهای نصب‌شده توسط کاربر و کتابخانه‌های مورد نیاز آنها است.

## 19. `/var`
- **English**: Contains files with changing content, such as logs, mail, and queues.
- **فارسی**: شامل فایل‌هایی است که محتوای آنها به صورت مداوم تغییر می‌کند، مانند لاگ‌های سیستم و فایل‌های صف‌ها.
