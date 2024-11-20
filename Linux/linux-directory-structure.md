# Linux Directory Structure (ساختار دایرکتوری لینوکس)

| Directory | English Description | توضیحات فارسی |
|-----------|----------------------|---------------|
| `/` (Root) | The root directory, the top-level directory in the filesystem. All other directories stem from here. | دایرکتوری ریشه یا همان Root که همه دایرکتوری‌های دیگر از آن منشعب می‌شوند. |
| `/bin` | Contains essential binaries that are necessary for the basic functioning of the system, like `ls`, `cp`, and `mv`. | شامل فایل‌های اجرایی (باینری‌ها) است که برای کارکردهای پایه سیستم مورد نیاز هستند. |
| `/boot` | Contains files necessary for booting the system, including the Linux kernel and bootloader configuration files. | شامل فایل‌های ضروری برای بوت شدن سیستم، از جمله کرنل لینوکس و فایل‌های پیکربندی بوت‌لودر. |
| `/dev` | Contains device files that represent hardware devices like disks, USB ports, etc. | شامل فایل‌های دستگاه (device files) است که نمایانگر دستگاه‌های سخت‌افزاری سیستم هستند. |
| `/etc` | Contains configuration files for the system, services, and applications. | شامل فایل‌های پیکربندی سیستم است. این دایرکتوری محل تنظیمات مربوط به سرویس‌ها و برنامه‌ها است. |
| `/home` | Contains home directories for users. Each user has a personal folder under this directory. | شامل دایرکتوری‌های کاربران است. هر کاربر یک پوشه جداگانه در این دایرکتوری دارد. |
| `/lib` | Contains shared libraries required by system programs and binaries. | شامل کتابخانه‌های اشتراکی (Shared Libraries) است که توسط برنامه‌ها و سیستم مورد استفاده قرار می‌گیرد. |
| `/media` | Used for mounting external devices like USB drives and CD/DVDs. Devices are automatically mounted here. | پوشه‌ای که برای مانت کردن دستگاه‌های خارجی مثل دیسک‌های USB و CD/DVD استفاده می‌شود. |
| `/mnt` | Used for manually mounting external filesystems. | به طور موقت برای مانت کردن فایل‌سیستم‌های خارجی به کار می‌رود. |
| `/opt` | Contains optional software, typically third-party applications not managed by the system's package manager. | دایرکتوری اختیاری که برای نصب نرم‌افزارهای شخص ثالث (third-party) استفاده می‌شود. |
| `/proc` | A virtual directory containing system and process information. | یک دایرکتوری مجازی که اطلاعات سیستم و فرآیندهای در حال اجرا را ذخیره می‌کند. |
| `/root` | The home directory of the root (administrator) user. | دایرکتوری خانگی کاربر root (کاربر اصلی سیستم). |
| `/run` | Contains runtime data such as process IDs and sockets. | یک دایرکتوری موقت که اطلاعات در حال اجرای سیستم را ذخیره می‌کند. |
| `/sbin` | Contains system binaries used for administrative tasks, typically only executable by the root user. | شامل دستورات سیستمی و مدیریتی (System Binaries) که معمولاً فقط توسط کاربر root اجرا می‌شوند. |
| `/srv` | Contains data for services provided by the system (e.g., web server files). | شامل داده‌های مربوط به سرویس‌های ارائه‌شده توسط سیستم است. |
| `/sys` | Another virtual directory, focusing on hardware information. | دایرکتوری مجازی دیگری که اطلاعات سخت‌افزاری و دستگاه‌های سیستم را نشان می‌دهد. |
| `/tmp` | Contains temporary files, which are usually deleted on reboot. | شامل فایل‌های موقتی است که توسط برنامه‌ها ایجاد می‌شوند. |
| `/usr` | Contains user-installed software and libraries. | شامل نرم‌افزارهای نصب‌شده توسط کاربر و کتابخانه‌های مورد نیاز آنها است. |
| `/var` | Contains files with changing content, such as logs, mail, and queues. | شامل فایل‌هایی است که محتوای آنها به صورت مداوم تغییر می‌کند، مانند لاگ‌های سیستم و فایل‌های صف‌ها. |
