Sistem Pakar Rekrutmen Software Engineer
Metode: Rule-Based Reasoning dengan Certainty Factor (Forward Chaining)

Deskripsi Proyek
Program ini merupakan sistem pakar sederhana yang digunakan untuk membantu proses seleksi calon Software Engineer.
Sistem akan menanyakan beberapa pertanyaan kepada pengguna terkait latar belakang pendidikan, pengalaman kerja, kemampuan teknis, serta soft skill.
Berdasarkan jawaban tersebut, sistem akan melakukan inferensi berbasis aturan (rule-based reasoning) dan menghitung tingkat keyakinan (certainty factor) untuk menentukan apakah kandidat LULUS atau TIDAK LULUS.


Struktur Program
- RULES → berisi kumpulan aturan (basis pengetahuan).
- parse_answer_to_cf() → mengubah jawaban pengguna menjadi nilai CF (0–1).
- combine_cf() → menggabungkan CF dari beberapa rule yang sama.
- evaluate_rules() → mengevaluasi aturan dan menentukan kesimpulan.
- ask_user_facts() → menampilkan pertanyaan ke pengguna.
- main() → menjalankan keseluruhan proses analisis.

Nama Anggota :
- Fikri Ahmad Arsalan (1313624039)
- Muhammad Azfa Hermawan (1313624040)
- Faiz Rifat Praditama (1313624041)
- Ahmad (1313624042)
- Muhammad (1313624043)
