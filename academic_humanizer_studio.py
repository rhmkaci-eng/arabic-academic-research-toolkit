# -*- coding: utf-8 -*-
"""
🏛️ استوديو مؤنسن ومطهّر الأسلوب الأكاديمي العربي (Arabic Academic Humanizer Studio)
واجهة بصرية تفاعلية عبر Gradio لتحليل وتطهير النصوص والبحوث الأكاديمية من بصمات الذكاء الاصطناعي،
وإنفاذ سمت أكابر النظار وضوابط كلية العلوم الإسلامية (خروبة - جامعة الجزائر 1).
"""

import sys
import os
import re
import gradio as gr

# ضبط الترميز على UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# إضافة مسار الأدوات للاستيراد
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from arabic_academic_humanizer import analyze_prose, quick_purify_rules
except ImportError:
    import arabic_academic_humanizer
    analyze_prose = arabic_academic_humanizer.analyze_prose
    quick_purify_rules = arabic_academic_humanizer.quick_purify_rules

# أمثلة تجريبية جاهزة للباحث
SAMPLE_AI_CLICHE = """مما لا شك فيه أن قضية السببية تلعب دوراً محورياً في الفلسفة الحديثة، ولا يخفى على أحد من الباحثين أن تسليط الضوء على هذه المسألة يشكل علامة فارقة. ومن الجدير بالذكر في هذا السياق المتصل أن هيوم قد قدم أطروحة مهمة، وتجدر الإشارة أيضاً إلى أن كانط قد تصدى له على صعيد آخر."""

SAMPLE_METHODOLOGY_VIOLATION = """نهدف في هذا المبحث إلى نقد المذهب التجريبي، وتفكيك بنية الشكوكية عند ديفيد هيوم ومحاكمة منطلقاته المعرفية. ونبين تهافت هذا الطرح عبر تفكيكية نقدية تستهدف نقده المعرفي وسجاله الكلامي."""

SAMPLE_LOANWORD_FLUFF = """تعتبر الرؤية التيليولوجية للعالم من أهم المباحث التي شهدت تحولاً كبيراً في منعطف التنوير. وأحسنتم وأجدتم في توجيه هذا الدليل الذي يُعد الضربة القاضية للإلحاد، وهو قدر الطاقة من أبرز المكتشفات الحديثة."""

# كود التنسيق المخصص RTL
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cairo:wght@400;600;700;800&display=swap');

* {
    font-family: 'Cairo', 'Amiri', 'Segoe UI', Tahoma, sans-serif !important;
}

body, .gradio-container {
    direction: rtl !important;
    text-align: right !important;
    background-color: #fbfbfb;
}

.rtl-box textarea {
    direction: rtl !important;
    text-align: right !important;
    font-size: 1.05rem !important;
    line-height: 1.8 !important;
}

.kalam-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    color: #f8fafc;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    border-bottom: 4px solid #eab308;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.kalam-header h1 {
    color: #facc15;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.kalam-header p {
    color: #cbd5e1;
    font-size: 1rem;
    margin: 0;
}

.score-badge {
    text-align: center;
    padding: 18px;
    border-radius: 12px;
    font-weight: 700;
    margin-bottom: 12px;
    border: 2px solid;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.score-high {
    background-color: #f0fdf4;
    border-color: #22c55e;
    color: #15803d;
}

.score-medium {
    background-color: #fefce8;
    border-color: #eab308;
    color: #a16207;
}

.score-low {
    background-color: #fef2f2;
    border-color: #ef4444;
    color: #b91c1c;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 14px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}

.metric-title {
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 4px;
}

.metric-val {
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a;
}
"""

def compute_ui_audit(raw_text):
    """دالة التحليل والتطهير للواجهة البصرية"""
    if not raw_text or not raw_text.strip():
        empty_badge = "<div class='score-badge score-medium'>⚠️ يرجى إدخال نص أولاً لتحليله وتطهيره.</div>"
        return empty_badge, "0", "0", "0.0", "", []

    report = analyze_prose(raw_text)
    purified = quick_purify_rules(raw_text)
    
    score = report['authenticity_score']
    if score >= 90:
        cls_name = "score-high"
        status_text = "💎 رصانة عالية: النص أصيل ومحكم كلامياً بنسبة ممتازة"
    elif score >= 70:
        cls_name = "score-medium"
        status_text = "⚠️ رصانة متوسطة: يحتوي النص على بعض الكليشيهات التي ينبغي تنقيحها"
    else:
        cls_name = "score-low"
        status_text = "🚨 تشبع بالذكاء الاصطناعي: النص مشبع بالكليشيهات والمخالفات المنهجية"

    score_html = f"""
    <div class='score-badge {cls_name}'>
        <div style='font-size: 2.2rem; font-weight: 800;'>{score} / 100</div>
        <div style='font-size: 1rem; margin-top: 4px;'>{status_text}</div>
    </div>
    """

    # إعداد جدول الملاحظات
    table_data = []
    for idx, f in enumerate(report['findings'], 1):
        table_data.append([
            f"{idx}",
            f"السطر {f['line']}",
            f['category'],
            f['matched'],
            f['advice'],
            f['snippet'][:80] + "..."
        ])

    return (
        score_html,
        str(report['total_words']),
        str(report['findings_count']),
        f"{report['cliche_density']}",
        purified,
        table_data
    )

def copy_to_clipboard_handler(text):
    """نسخ النص إلى حافظة الويندوز مباشرة عبر pyperclip"""
    if not text or not text.strip():
        return "⚠️ لا يوجد نص مؤنسن لنسخه!"
    try:
        import pyperclip
        pyperclip.copy(text)
        return "✅ تم نسخ النص المؤنسن إلى الحافظة بنجاح! الصقه في Word (Ctrl+V)."
    except Exception as e:
        return f"❌ تعذر النسخ الآلي: {str(e)}"

def process_uploaded_file(file_obj):
    """معالجة ملف ماركداون أو نصي مرفوع"""
    if file_obj is None:
        return "⚠️ يرجى رفع ملف صالح.", "", [], None
    
    file_path = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    score_html, w_count, f_count, dens, purified, table_data = compute_ui_audit(content)
    
    # حفظ الملف المطهر للتحميل
    out_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    purified_filename = f"{base_name}_purified.md"
    purified_filepath = os.path.join(out_dir, purified_filename)
    
    with open(purified_filepath, 'w', encoding='utf-8') as f:
        f.write(purified)

    summary_text = f"✅ تم فحص الملف بنجاح! ({w_count} كلمة | {f_count} مواضع رصد)"
    return summary_text, purified, table_data, purified_filepath

def build_app():
    with gr.Blocks(title="استوديو مؤنسن الأسلوب الأكاديمي العربي") as demo:
        # الترويسة الرئيسية
        gr.HTML("""
        <div class='kalam-header'>
            <h1>🏛️ استوديو مؤنسن ومطهّر الأسلوب الأكاديمي العربي</h1>
            <p>المنظومة التطبيقية لتحرير وتطهير المسودات والبحوث الأكاديمية من بصمات الذكاء الاصطناعي وإنفاذ سمت أكابر النظار</p>
        </div>
        """)

        with gr.Tabs():
            # التبويب الأول: الأنسنة المباشرة للنصوص
            with gr.TabItem("✨ الأنسنة والتطهير الفوري للنصوص"):
                with gr.Row():
                    with gr.Column(scale=5):
                        input_text = gr.Textbox(
                            label="📥 نص المسودة أو المقطع المراد تحليله وتطهيره",
                            placeholder="الصق نص المسودة هنا لفحصها وتطهيرها من بصمات الذكاء الاصطناعي وركاكة التوليد الآلي...",
                            lines=10,
                            elem_classes=["rtl-box"]
                        )
                        with gr.Row():
                            btn_sample1 = gr.Button("📋 تجربة: كليشيهات الذكاء الاصطناعي", size="sm")
                            btn_sample2 = gr.Button("📋 تجربة: حظر النقد والتفكيك", size="sm")
                            btn_sample3 = gr.Button("📋 تجربة: الرطانة والمكياج", size="sm")

                        with gr.Row():
                            btn_clear = gr.Button("🗑️ مسح", size="sm", variant="secondary")
                            btn_purify = gr.Button("🚀 فحص وتطهير النص الأكاديمي", size="lg", variant="primary")

                    with gr.Column(scale=5):
                        score_output = gr.HTML("<div class='score-badge score-medium'>اضغط «فحص وتطهير النص الأكاديمي» لبدء التحليل.</div>")
                        with gr.Row():
                            with gr.Column(scale=1):
                                gr.HTML("<div class='metric-title'>إجمالي الكلمات</div>")
                                words_output = gr.Label(value="0", show_label=False)
                            with gr.Column(scale=1):
                                gr.HTML("<div class='metric-title'>البصمات المرصودة</div>")
                                findings_output = gr.Label(value="0", show_label=False)
                            with gr.Column(scale=1):
                                gr.HTML("<div class='metric-title'>كثافة الكليشيهات / 1000 كلمة</div>")
                                density_output = gr.Label(value="0.0", show_label=False)

                        output_text = gr.Textbox(
                            label="📤 النص المؤنسن والمطهر أولياً",
                            lines=10,
                            elem_classes=["rtl-box"]
                        )
                        with gr.Row():
                            btn_copy_clip = gr.Button("📋 نسخ النص المؤنسن إلى الحافظة (Clipboard)", variant="secondary", size="sm")
                            copy_status = gr.Label(value="", show_label=False)

                gr.HTML("<h3 style='margin-top: 24px; color: #1e293b;'>🔍 جدول الانتهاكات والبصمات المرصودة تفصيلاً:</h3>")
                findings_table = gr.Dataframe(
                    headers=["#", "الموضع", "التصنيف المنهجي", "اللفظ المرصود", "التوجيه والبديل المعتمد", "سياق العبارة"],
                    datatype=["str", "str", "str", "str", "str", "str"],
                    column_count=(6, "fixed"),
                    wrap=True
                )

                # ربط أزرار النماذج
                btn_sample1.click(fn=lambda: SAMPLE_AI_CLICHE, outputs=input_text)
                btn_sample2.click(fn=lambda: SAMPLE_METHODOLOGY_VIOLATION, outputs=input_text)
                btn_sample3.click(fn=lambda: SAMPLE_LOANWORD_FLUFF, outputs=input_text)
                btn_clear.click(fn=lambda: ("", "<div class='score-badge score-medium'>يرجى إدخال نص للتحليل.</div>", "0", "0", "0.0", "", [], ""), 
                                outputs=[input_text, score_output, words_output, findings_output, density_output, output_text, findings_table, copy_status])

                # تنفيذ الفحص
                btn_purify.click(
                    fn=compute_ui_audit,
                    inputs=input_text,
                    outputs=[score_output, words_output, findings_output, density_output, output_text, findings_table]
                )

                # زر النسخ للحافظة
                btn_copy_clip.click(
                    fn=copy_to_clipboard_handler,
                    inputs=output_text,
                    outputs=copy_status
                )

            # التبويب الثاني: تطهير وفحص الملفات الكاملة
            with gr.TabItem("📁 فحص وتطهير ملفات المسودات (Markdown / TXT)"):
                gr.Markdown("قم برفع ملف مسودة البحث (`.md` أو `.txt`) لفحصه كاملاً واستخراج تقرير مفصل وتنزيل النسخة المطهرة.")
                with gr.Row():
                    file_input = gr.File(label="رفع ملف المسودة (.md / .txt)", file_types=[".md", ".txt"])
                
                btn_file_process = gr.Button("🔍 فحص وتطهير الملف المرفوع", variant="primary", size="lg")
                file_summary_html = gr.HTML()
                
                with gr.Row():
                    file_purified_preview = gr.Textbox(
                        label="معاينة النص المطهر داخل الملف",
                        lines=12,
                        elem_classes=["rtl-box"]
                    )
                
                file_download = gr.File(label="📥 تحميل الملف المطهر")
                file_table = gr.Dataframe(
                    headers=["#", "الموضع", "التصنيف المنهجي", "اللفظ المرصود", "التوجيه والبديل المعتمد", "سياق العبارة"],
                    datatype=["str", "str", "str", "str", "str", "str"],
                    column_count=(6, "fixed"),
                    wrap=True
                )

                btn_file_process.click(
                    fn=process_uploaded_file,
                    inputs=file_input,
                    outputs=[file_summary_html, file_purified_preview, file_table, file_download]
                )

            # التبويب الثالث: ميثاق السمت الأكاديمي وقواعد النظار
            with gr.TabItem("📜 ميثاق السمت الأكاديمي وقواعد النظار"):
                gr.Markdown("""
                <div style='line-height: 2; font-size: 1.05rem; padding: 12px;'>

                ### ⚖️ الأصول الأربعة المعتمدة في مؤنسن ومطهّر الأسلوب الأكاديمي:

                #### 1. حظر مصطلحي «النقد» و«التفكيك» والالتزام الحصري بـ «التحليل»:
                * **العلة الكلامية:** النقد ينطوي على نبرة قضائية وخصومة مسبقة تصرف البحث عن التجرد العلمي. والتفكيك يحمل إحالات عدمية وما بعد حداثية تُسقط موثوقية البراهين.
                * **البديل المعتمد دائماً:** **«التحليل»**، **«الفحص التحليلي»**، **«الفحص والتحليل الكلامي والإبستمولوجي»**.

                #### 2. اجتثاث كليشيهات الذكاء الاصطناعي وحشوه المعلب:
                * **الألفاظ المحظورة:** «مما لا شك فيه»، «لا يخفى على أحد»، «من نافلة القول»، «يلعب دوراً محورياً»، «يسلط الضوء على»، «من الجدير بالذكر»، «في هذا السياق المتصل».
                * **المنهج الأكاديمي:** الدخول في صلب المسألة والمطالب رأساً دون ديباجات أو فضول لفظي؛ فالبلاغة الإيجاز، وكلام النظار كالمعادلات الرياضية لا فضل فيه للفظ على المعنى.

                #### 3. تعريب الرطانة الفلسفية والمصطلحات المستغربة:
                * **المعايير المعتمدة:**
                  * استبدال **«التيليولوجية»** بـ **«الجهة الغائية»** أو **«مبحث الغائية والحكمة»**.
                  * استبدال **«منعطف التنوير»** بـ **«عصر التنوير»**.
                  * استبدال **«الأنطولوجي»** في سياق إثبات الصانع بـ **«البرهان الوجودي»**.

                #### 4. حظر مكياج المتكلمين والتزويق الإنشائي:
                * **الضابط:** منع السجع المتكلف، والأوصاف الاستعراضية («الضربة القاضية»، «الرد المفحم»، «الفارس الهمام»)، وحصر قيد **«قدر الطاقة»** في جهد الباحث الذاتي دون إلحاقه بالظواهر والمصنفات الخارجية.
                
                </div>
                """)

    return demo

def launch_studio(port=7865):
    app = build_app()
    print(f"🚀 جاري إطلاق استوديو مؤنسن الأسلوب الأكاديمي العربي على http://127.0.0.1:{port} ...")
    app.launch(server_name="127.0.0.1", server_port=port, css=CUSTOM_CSS, theme=gr.themes.Soft(), show_error=True)

if __name__ == "__main__":
    launch_studio()
