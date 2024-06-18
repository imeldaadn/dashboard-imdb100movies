import streamlit as st
import pandas as pd
import plotly.express as px
from numerize.numerize import numerize

# Konfigurasi halaman
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dashboard
st.header('Hi, Welcome to the :blue[**Data Visualization Dashboard!**]')
st.markdown('We are here to showcase your data :orange[in] a cool :orange[and] engaging way :sunglasses:')
st.subheader("IMDB - Movies 100 Years by Users")

# Load Data
df = pd.read_csv("src/movies100_combined_data.csv")
df["Year"] = df["Year"].astype(int) # Convert Year to int

# Sidebar
st.sidebar.image("src/logoupnbaru.png", caption="Imelda Audina - 21082010003 - Sistem Informasi - Fakultas Ilmu Komputer")
st.sidebar.title('🛒 Data Visualization Dashboard')

# Filter
st.sidebar.header("Filter: ")
rating = st.sidebar.multiselect(
    "Pilih Rating:", 
    options = df["Rating"].unique(),
    default = df["Rating"].unique()
)

# Input tahun awal dan akhir
start_year = st.sidebar.number_input("Tahun Mulai", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=int(df["Year"].min()))
end_year = st.sidebar.number_input("Tahun Akhir", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=int(df["Year"].max()))

# Filter DataFrame
df_selection = df[
    (df["Rating"].isin(rating)) &
    (df["Year"] >= start_year) &
    (df["Year"] <= end_year)
]

# Fungsi Home untuk menampilkan data
def Home():
    with st.expander("Table Data"):
        showData = st.multiselect('Filter Kolom: ', df_selection.columns, default=df_selection.columns.tolist())
        st.write(df_selection[showData])

Home()

# Fungsi untuk menampilkan grafik bar chart - comparisson
container1 = st.container(border=True)
def graphs1():
    # Bar Chart
    fig_bar = px.bar(
        df_selection, 
        x='Year', 
        y='Gross_World', 
        title='Bar Chart: Gross Earnings by Year - Comparisson',
        labels={'Gross_World': 'Gross World Earnings ($)', 'Year': 'Year'},
        color='Year',
        hover_data=['Name']
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_bar)

# Fungsi untuk analisis data
def analysis1():
    with st.expander("Analysis", expanded=False):
        total_gross_by_year = df_selection.groupby("Year")[["Gross_World"]].sum().sort_values(by="Gross_World")
        max_year = total_gross_by_year.idxmax().values[0]
        min_year = total_gross_by_year.idxmin().values[0]
        total_gross = total_gross_by_year["Gross_World"].sum()
        
        st.markdown('**Total Gross Earnings**')
        st.write(f"Total pendapatan kotor dari {start_year} hingga {end_year} adalah {numerize(int(total_gross))}.")
        st.markdown('')

        st.markdown('**Pendapatan Kotor Berdasarkan Tahun**')
        st.write(f"Tahun dengan pendapatan kotor tertinggi adalah **{max_year}** dengan total pendapatan sebesar {numerize(int(total_gross_by_year.loc[max_year, 'Gross_World']))}.")
        st.write(f"Tahun dengan pendapatan kotor terendah adalah **{min_year}** dengan total pendapatan sebesar {numerize(int(total_gross_by_year.loc[min_year, 'Gross_World']))}.")
        st.markdown('**Detail Analisis**')
        st.write(f"Terdapat perbedaan yang signifikan dalam pendapatan kotor dari tahun ke tahun. Beberapa faktor yang dapat mempengaruhi hal ini termasuk popularitas film yang dirilis, strategi pemasaran, dan perubahan tren penonton. Menariknya, pada tahun **{max_year}**, ada kemungkinan besar bahwa film-film blockbuster dengan anggaran besar dirilis, yang berkontribusi pada tingginya pendapatan. Sebaliknya, pada tahun **{min_year}**, mungkin ada lebih sedikit film besar atau mungkin terjadi penurunan minat penonton.")

# Fungsi untuk menampilkan grafik scatter plot - relationship
container2 = st.container(border=True)
def graphs2():
    # Scatter Plot
    fig_scatter = px.scatter(
        df_selection,
        x='Budget',
        y='Gross_World',
        size='Gross_World',
        color='Rating',
        hover_name='Name',
        title='<b>Scatter Plot: Between Budget and Gross World Earnings - Relationship</b>',
        labels={'Budget': 'Budget ($)', 'Gross_World': 'Gross World Earnings ($)'},
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_scatter)

# Fungsi untuk analisis data scatter plot
def analysis2():
    with st.expander("Analysis", expanded=False):
        st.markdown('**Relationship between Budget and Gross World Earnings**')
        st.write("Scatter plot ini menunjukkan hubungan antara anggaran (budget) dan pendapatan kotor dunia (gross world earnings). Dari grafik ini, kita dapat melihat bahwa ada kecenderungan bahwa film dengan anggaran yang lebih tinggi cenderung memiliki pendapatan kotor yang lebih tinggi. Namun, terdapat juga beberapa film dengan anggaran rendah yang berhasil meraih pendapatan kotor tinggi, menunjukkan bahwa faktor lain seperti cerita, pemasaran, dan popularitas juga berperan penting.")
        
        st.markdown('**Detail Analisis**')
        st.write("Film-film dengan anggaran besar (ditandai dengan titik-titik yang lebih besar) cenderung mendominasi di sisi kanan atas grafik, menunjukkan bahwa anggaran yang besar seringkali diikuti oleh pendapatan yang besar. Namun, ada juga film-film dengan anggaran lebih rendah yang menunjukkan performa luar biasa dalam hal pendapatan kotor dunia. Misalnya, beberapa film dengan anggaran sedang atau rendah tetapi dengan cerita yang kuat dan pemasaran yang efektif berhasil mencapai pendapatan tinggi. Ini menunjukkan bahwa sukses sebuah film tidak hanya tergantung pada anggaran, tetapi juga berbagai faktor lain seperti kualitas film dan strategi pemasaran.")
        
# Fungsi untuk menampilkan grafik treemap - composition
container3 = st.container(border=True)
def graphs3():
    # Treemap
    fig_treemap = px.treemap(
        df_selection,
        path=['Rating', 'Name'],
        values='Gross_World',
        title='<b>Treemap: Composition of Gross World Earnings by Rating and Movie - Composition</b>',
        labels={'Gross_World': 'Gross World Earnings ($)'}
    )
    fig_treemap.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_treemap)

# Fungsi untuk analisis data treemap
def analysis3():
    with st.expander("Analysis", expanded=False):
        st.markdown('**Composition of Gross World Earnings by Rating and Movie**')
        st.write("Treemap ini menunjukkan komposisi pendapatan kotor dunia berdasarkan rating dan film. Dari grafik ini, kita dapat melihat bagaimana pendapatan kotor terdistribusi di antara berbagai rating dan film.")
        
        st.markdown('**Detail Analisis**')
        st.write("Dari treemap, kita dapat melihat bahwa film dengan rating tertentu mendominasi dalam hal pendapatan kotor. Misalnya, film dengan rating yang lebih tinggi mungkin menunjukkan area yang lebih besar dalam treemap, menandakan pendapatan kotor yang lebih tinggi. Ini dapat menunjukkan bahwa film dengan rating lebih tinggi cenderung lebih sukses secara finansial. Namun, ada juga film dengan rating lebih rendah yang menunjukkan performa luar biasa dalam hal pendapatan, menunjukkan bahwa faktor lain seperti popularitas film, pemasaran, dan tren penonton juga berperan penting.")

# Fungsi untuk menampilkan grafik histogram - distribusi durasi film
container4 = st.container(border=True)
def graphs4():
    # Histogram Durasi Film
    fig_hist = px.histogram(
        df,
        x='Durasi(Menit)',
        title='<b>Histogram: Distribusi Durasi Film - Distribution</b>',
        labels={'Durasi(Menit)': 'Durasi (Menit)'},
        marginal='box'
    )
    fig_hist.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_hist)

# Fungsi untuk analisis data histogram
def analysis4():
    with st.expander("Analysis", expanded=False):
        st.markdown('**Distribusi Durasi Film**')
        st.write("Histogram ini menunjukkan distribusi durasi film dalam menit dari data film yang dipilih. Dari grafik ini, kita dapat melihat bagaimana durasi film terdistribusi di antara film-film tersebut.")
        
        st.markdown('**Detail Analisis**')
        mean_duration = df['Durasi(Menit)'].mean()
        median_duration = df['Durasi(Menit)'].median()
        mode_duration = df['Durasi(Menit)'].mode().values[0]
        st.write(f"Durasi rata-rata film adalah {mean_duration:.2f} menit.")
        st.write(f"Durasi median film adalah {median_duration:.2f} menit.")
        st.write(f"Durasi modus film adalah {mode_duration} menit.")
        
        st.write("Dari histogram, kita dapat melihat beberapa hal:")
        st.write("- **Sebaran Durasi Film**: Distribusi durasi film cenderung normal dengan sebagian besar film memiliki durasi antara 90 hingga 120 menit.")
        st.write("- **Outlier**: Ada beberapa film yang memiliki durasi sangat pendek atau sangat panjang yang terlihat sebagai outlier di histogram.")
        st.write("- **Durasi Populer**: Durasi film yang paling umum adalah sekitar 100 menit, yang merupakan durasi standar bagi kebanyakan film fitur.")
        
        st.write("Distribusi ini memberikan wawasan tentang durasi film yang diproduksi dan bagaimana durasi tersebut mempengaruhi kategori dan genre film. Film dengan durasi yang lebih panjang cenderung memiliki lebih banyak plot dan pengembangan karakter, sementara film dengan durasi yang lebih pendek biasanya lebih fokus dan cepat tempo.")

with container1:
    graphs1()
    analysis1()

with container2:
    graphs2()
    analysis2()

with container3:
    graphs3()
    analysis3()

with container4:
    graphs4()
    analysis4()