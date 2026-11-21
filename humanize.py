# -*- coding: utf-8 -*-
"""
🏛️ أداة الأنسنة الموحدة للبحوث الأكاديمية (Unified Academic Humanizer CLI)
الواجهة التنفيذية الشاملة لجميع أنماط استخدام مؤنسن ومطهر الأسلوب الأكاديمي العربي.

الأنماط المدعومة:
1. فحص ملف مفرد أو نص مباشر:
   python tools/humanize.py "article.md"
2. التطهير المباشر داخل نفس الملف مع نسخة احتياطية:
   python tools/humanize.py "article.md" --in-place
3. نمط الحافظة السريع (Clipboard):
   python tools/humanize.py --clip
4. تشغيل استوديو الأنسنة البصري التفاعلي في المتصفح:
   python tools/humanize.py --ui
5. مراقبة مجلد الأبحاث حياً وتطهير أي مسودة تُحفظ تلقائياً:
   python tools/humanize.py --watch "./research_drafts"
"""

import sys
import os
import time
import argparse
import shutil

# ضبط المخرجات على UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# استيراد محرك الأنسنة المركزي
parent_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(os.path.dirname(parent_dir), '.agents', 'skills', 'academic-research-methodology', 'scripts')
sys.path.append(scripts_dir)
sys.path.append(parent_dir)

try:
    from arabic_academic_humanizer import analyze_prose, quick_purify_rules
except ImportError:
    # محاولة الاستيراد المحلي
    import arabic_academic_humanizer
    analyze_prose = arabic_academic_humanizer.analyze_prose
    quick_purify_rules = arabic_academic_humanizer.quick_purify_rules

def run_clipboard_humanizer():
    """تطهير فوري لمحتوى الحافظة الحالية وإعادة النص المؤنسن إليها"""
    try:
        import pyperclip
    except ImportError:
        print("❌ حزمة pyperclip غير مثبتة. يرجى تشغيل: pip install pyperclip")
        return False

    raw_text = pyperclip.paste()
    if not raw_text or not raw_text.strip():
        print("⚠️ الحافظة فارغة! انسخ نصاً أولاً ثم أعد تشغيل الأمر.")
        return False

    print("📋 جاري فحص وتطهير النص الموجود في الحافظة...")
    report = analyze_prose(raw_text)
    
    print("\n" + "="*55)
    print("🏛️ تقرير الأنسنة السريع للحافظة (Quick Clipboard Audit)")
    print("="*55)
    print(f"📊 عدد الكلمات: {report['total_words']}")
    print(f"⚠️ بصمات الذكاء الاصطناعي المرصودة: {report['findings_count']}")
    print(f"💎 مؤشر الرصانة والأصالة: {report['authenticity_score']} / 100")
    print("="*55)

    purified = quick_purify_rules(raw_text)
    pyperclip.copy(purified)
    
    print("\n✅ تم بنجاح! تم تطهير النص ووضعه في الحافظة.")
    print("👉 اضغط الآن (Ctrl + V) في مستند Word أو Obsidian للصق النص المؤنسن.")
    return True

def run_file_humanizer(filepath, in_place=False, output=None):
    """فحص أو تطهير ملف ماركداون أو نصي"""
    if not os.path.exists(filepath):
        print(f"❌ الملف غير موجود: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    report = analyze_prose(content)
    
    print("\n" + "="*65)
    print(f"🏛️ تقرير فحص الملف: {os.path.basename(filepath)}")
    print("="*65)
    print(f"📊 إجمالي الكلمات: {report['total_words']}")
    print(f"⚠️ مواضع الركاكة والـ AI: {report['findings_count']}")
    print(f"📈 كثافة الكليشيهات: {report['cliche_density']} / 1000 كلمة")
    print(f"💎 مؤشر الرصانة والأصالة: {report['authenticity_score']} / 100")
    print("="*65)

    if report['findings']:
        print("\n🔍 أبرز الملاحظات المرصودة:")
        for idx, f in enumerate(report['findings'][:15], 1):
            print(f" [{idx:02d}] السطر {f['line']} | {f['category']}:")
            print(f"      اللفظ المرصود: «{f['matched']}»")
            print(f"      التوجيه: {f['advice']}")
            print(f"      السياق: {f['snippet'][:75]}...\n")
        if len(report['findings']) > 15:
            print(f"... وتم طي {len(report['findings']) - 15} موضعاً إضافياً للتركيز.")
    else:
        print("✅ الملف سليم 100% وخالٍ من بصمات الذكاء الاصطناعي.")

    if in_place or output:
        # إنشاء نسخة احتياطية
        if in_place:
            bak_path = filepath + ".bak"
            shutil.copy2(filepath, bak_path)
            target_out = filepath
            print(f"🔒 تم إنشاء نسخة احتياطية في: {os.path.basename(bak_path)}")
        else:
            target_out = output

        purified = quick_purify_rules(content)
        with open(target_out, 'w', encoding='utf-8') as f:
            f.write(purified)
        print(f"💾 تم حفظ النص المؤنسن في: {target_out}")
    return True

def run_folder_watcher(folder_path):
    """مراقبة حية لمجلد أبحاث وتنبيه الباحث عند حفظ أي مسودة تحتوي كليشيهات AI"""
    if not os.path.exists(folder_path):
        print(f"❌ المجلد غير موجود: {folder_path}")
        return False

    print(f"👀 بدء المراقبة الحية للمجلد: {folder_path}")
    print("   (سيتولى النظام فحص أي ملف .md أو .txt يتم تعديله فورياً)")
    print("   اضغط Ctrl + C لإيقاف المراقبة.")
    
    file_mtimes = {}
    try:
        while True:
            for root, dirs, files in os.walk(folder_path):
                for fname in files:
                    if fname.endswith(('.md', '.txt')) and not fname.endswith('.bak'):
                        fpath = os.path.join(root, fname)
                        mtime = os.path.getmtime(fpath)
                        if fpath in file_mtimes:
                            if mtime > file_mtimes[fpath]:
                                file_mtimes[fpath] = mtime
                                print(f"\n⚡ رصد تعديل جديد في: {fname}")
                                run_file_humanizer(fpath)
                        else:
                            file_mtimes[fpath] = mtime
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف مراقبة المجلد.")

def main():
    parser = argparse.ArgumentParser(description="Unified Academic Humanizer CLI for Future Research")
    parser.add_argument("target", nargs="?", help="مسار الملف أو النص المباشر المراد فحصه")
    parser.add_argument("--clip", "-c", action="store_true", help="فحص وتطهير الحافظة الفورية (Clipboard)")
    parser.add_argument("--in-place", "-i", action="store_true", help="تطبيق التطهير وحفظ النتيجة في نفس الملف مباشرة مع أخذ نسخة احتياطية")
    parser.add_argument("--output", "-o", help="مسار حفظ النتيجة المصححة في ملف جديد")
    parser.add_argument("--ui", "-u", action="store_true", help="تشغيل استوديو الأنسنة البصري في المتصفح")
    parser.add_argument("--watch", "-w", help="مراقبة حية لمجلد أبحاث معين")
    
    args = parser.parse_args()

    if args.ui:
        studio_path = os.path.join(parent_dir, "academic_humanizer_studio.py")
        if os.path.exists(studio_path):
            os.system(f'python "{studio_path}"')
        else:
            print("❌ استوديو الأنسنة غير موجود في المسار المتوقع.")
        return

    if args.clip:
        run_clipboard_humanizer()
        return

    if args.watch:
        run_folder_watcher(args.watch)
        return

    if args.target:
        if os.path.exists(args.target):
            run_file_humanizer(args.target, in_place=args.in_place, output=args.output)
        else:
            # معالجة كنص مباشر
            report = analyze_prose(args.target)
            print("\n" + "="*55)
            print("🏛️ تقرير الأنسنة للنص المباشر:")
            print("="*55)
            print(f"📊 عدد الكلمات: {report['total_words']}")
            print(f"⚠️ البصمات المرصودة: {report['findings_count']}")
            print(f"💎 مؤشر الأصالة: {report['authenticity_score']} / 100")
            print("="*55)
            purified = quick_purify_rules(args.target)
            print("\n📝 النص المؤنسن:")
            print(purified)
        return

    parser.print_help()

if __name__ == '__main__':
    main()
