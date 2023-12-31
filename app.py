import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetch unique user
    user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words,num_media_messages = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3= st._main.columns(3)


        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(daily_timeline['date_only'],daily_timeline['message'],color='darkgreen')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2=st._main.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values,color='blueviolet')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index,busy_month.values,color='turquoise')
            st.pyplot(fig)

        user_heatmap=helper.activity_heatmap(selected_user,df)
        st.title('Weekly Activity Heatmap')
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #finding the busy users in the grp
        if selected_user =='overall':
            st.title('Most Busy Users')
            x,new_df=helper.most_busy_users(df)
            fig, ax =plt.subplots()

            col1,col2=st._main.columns(2)

            with col1:
                 ax.bar(x.index,x.values,color='crimson')
                 plt.xticks(rotation='vertical')
                 st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #wordcloud
        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='yellowgreen')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)


        #emoji analyss
        emoji_df= helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 =st._main.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

