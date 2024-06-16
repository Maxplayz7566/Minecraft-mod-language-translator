import sys
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QScrollArea, QCheckBox, QPushButton, QFileDialog
from deep_translator import GoogleTranslator
import json

Languages = {
    "en": ["English (Copy to folder)", "en_us.json"],
    "de": ["German", "de_de.json"],
    "fr": ["French", "fr_fr.json"],
    "it": ["Italian", "it_it.json"],
    "es": ["Spanish", "es_es.json"],
    "pt": ["Portuguese", "pt_br.json"],
    "nl": ["Dutch", "nl_nl.json"],
    "ru": ["Russian", "ru_ru.json"],
    "zh-CN": ["Chinese", "zh_cn.json"],
    "ja": ["Japanese", "ja_jp.json"],
    "ko": ["Korean", "ko_kr.json"],
    "ar": ["Arabic", "ar_sa.json"],
    "tr": ["Turkish", "tr_tr.json"],
    "hi": ["Hindi", "hi_in.json"],
    "th": ["Thai", "th_th.json"],
    "vi": ["Vietnamese", "vi_vn.json"],
    "fi": ["Finnish", "fi_fi.json"],
    "sv": ["Swedish", "sv_se.json"],
    "no": ["Norwegian", "no_no.json"],
    "da": ["Danish", "da_dk.json"],
    "el": ["Greek", "el_gr.json"],
    "bg": ["Bulgarian", "bg_bg.json"],
    "cs": ["Czech", "cs_cz.json"],
    "et": ["Estonian", "et_ee.json"],
    "hr": ["Croatian", "hr_hr.json"],
    "hu": ["Hungarian", "hu_hu.json"],
    "id": ["Indonesian", "id_id.json"],
    "lt": ["Lithuanian", "lt_lt.json"],
    "lv": ["Latvian", "lv_lv.json"],
    "ms": ["Malay", "ms_my.json"],
    "pl": ["Polish", "pl_pl.json"],
    "ro": ["Romanian", "ro_ro.json"],
    "sk": ["Slovak", "sk_sk.json"],
    "sl": ["Slovenian", "sl_si.json"],
    "uk": ["Ukrainian", "uk_ua.json"],
    "af": ["Afrikaans", "af_za.json"],
    "sq": ["Albanian", "sq_al.json"],
    "am": ["Amharic", "am_et.json"],
    "hy": ["Armenian", "hy_am.json"],
    "az": ["Azerbaijani", "az_az.json"],
    "eu": ["Basque", "eu_es.json"],
    "be": ["Belarusian", "be_by.json"],
    "bn": ["Bengali", "bn_bd.json"],
    "bs": ["Bosnian", "bs_ba.json"],
    "ceb": ["Cebuano", "ceb_ph.json"],
    "ny": ["Chichewa", "ny.json"],
    "co": ["Corsican", "co_fr.json"],
    "ht": ["Haitian Creole", "ht_ht.json"],
    "haw": ["Hawaiian", "haw_us.json"],
    "iw": ["Hebrew", "iw_il.json"],
    "jw": ["Javanese", "jw_jw.json"],
    "kn": ["Kannada", "kn_in.json"],
    "kk": ["Kazakh", "kk_kz.json"],
    "km": ["Khmer", "km_kh.json"],
    "rw": ["Kinyarwanda", "rw_rw.json"],
    "ku": ["Kurdish (Kurmanji)", "ku_ku.json"],
    "ky": ["Kyrgyz", "ky_ky.json"],
    "lo": ["Lao", "lo_la.json"],
    "la": ["Latin", "la_la.json"],
    "lb": ["Luxembourgish", "lb_lu.json"],
    "mk": ["Macedonian", "mk_mk.json"],
    "mg": ["Malagasy", "mg_mg.json"],
    "ml": ["Malayalam", "ml_in.json"],
    "mt": ["Maltese", "mt_mt.json"],
    "mi": ["Maori", "mi_nz.json"],
    "mr": ["Marathi", "mr_in.json"],
    "mn": ["Mongolian", "mn_mn.json"],
    "my": ["Myanmar (Burmese)", "my_mm.json"],
    "ne": ["Nepali", "ne_np.json"],
    "or": ["Odia (Oriya)", "or_in.json"],
    "ps": ["Pashto", "ps_af.json"],
    "fa": ["Persian", "fa_ir.json"],
    "pa": ["Punjabi", "pa_in.json"],
    "sm": ["Samoan", "sm_ws.json"],
    "gd": ["Scottish Gaelic", "gd_gb.json"],
    "sr": ["Serbian", "sr_rs.json"],
    "st": ["Sesotho", "st_ls.json"],
    "sn": ["Shona", "sn_zw.json"],
    "sd": ["Sindhi", "sd_in.json"],
    "si": ["Sinhala", "si_lk.json"],
    "so": ["Somali", "so_so.json"],
    "su": ["Sundanese", "su_id.json"],
    "tl": ["Filipino", "tl_ph.json"],
    "tg": ["Tajik", "tg_tj.json"],
    "ta": ["Tamil", "ta_in.json"],
    "te": ["Telugu", "te_in.json"],
    "tr": ["Turkmen", "tr_tm.json"],
    "ug": ["Uyghur", "ug_cn.json"],
    "uz": ["Uzbek", "uz_uz.json"],
    "cy": ["Welsh", "cy_gb.json"],
    "xh": ["Xhosa", "xh_za.json"],
    "yi": ["Yiddish", "yi_us.json"],
    "yo": ["Yoruba", "yo_ng.json"],
    "zu": ["Zulu", "zu_za.json"]
}

selected_languages = []


def translate_file(output_folder):
    try:
        input_file = "en_us.json"
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        def translate(language_code):
            try:
                output_file = f"{output_folder}/{Languages[language_code][1]}"
                translator = GoogleTranslator(source='en', target=language_code)
                translated_data = translator.translate_batch(list(data.values()))

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(dict(zip(data.keys(), translated_data)), f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Error occurred: {e} on language {language_code}")

        for language_code in selected_languages:
            thread = threading.Thread(target=lambda: translate(language_code))
            thread.start()

        print("Translation completed!")

    except Exception as e:
        print(f"Error occurred: {e}")


def on_checkbox_change(language_code, checkbox, var):
    if checkbox.isChecked():
        selected_languages.append(language_code)
    elif language_code in selected_languages:
        selected_languages.remove(language_code)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translate en_us.json to other languages")
        self.setGeometry(100, 100, 500, 500)
        self.initialize_gui()

    def initialize_gui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title = QLabel("Translate en_us.json to other languages!")
        title.setFont(title.font())
        layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)

        self.checkbox_list = []

        for language_code, language_info in Languages.items():
            checkbox = QCheckBox(language_info[0])
            checkbox.stateChanged.connect(lambda state, lc=language_code, cb=checkbox: on_checkbox_change(lc, cb, state))
            scroll_layout.addWidget(checkbox)
            self.checkbox_list.append(checkbox)

        layout.addWidget(scroll_area)

        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_languages)
        layout.addWidget(select_all_button)

        translate_button = QPushButton("Translate")
        translate_button.clicked.connect(self.choose_output_folder)
        layout.addWidget(translate_button)

    def select_all_languages(self):
        for checkbox in self.checkbox_list:
            checkbox.setChecked(True)

    def choose_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder:
            translate_file(output_folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
