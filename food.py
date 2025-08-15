import streamlit as st
import pandas as pd

# ---------------------------
# Load data
# ---------------------------
@st.cache_data
def load_data():
    providers = pd.read_csv("providers_data.csv")
    receivers = pd.read_csv("receivers_data.csv")
    claims = pd.read_csv("claims_data.csv")
    listings = pd.read_csv("food_listings_data.csv")
    return providers, receivers, claims, listings

providers, receivers, claims, listings = load_data()

# Ensure numeric
listings["Quantity"] = pd.to_numeric(listings["Quantity"], errors="coerce")
claims["Quantity"] = claims["Food_ID"].map(
    listings.set_index("Food_ID")["Quantity"]
)  # map quantities from listings

# ---------------------------
# Dashboard title
# ---------------------------
st.title("🍽️ Food Donation Dashboard")
st.markdown("Interactive analytics for Providers, Receivers, Listings & Claims")

# ---------------------------
# Question 1: Providers & Receivers per city
# ---------------------------
st.header("1️⃣ Providers & Receivers in Each City")
city_data = pd.DataFrame({
    "Providers": providers.groupby("City")["Provider_ID"].nunique(),
    "Receivers": receivers.groupby("City")["Receiver_ID"].nunique()
}).fillna(0).astype(int)
st.dataframe(city_data)

# ---------------------------
# Question 2: Provider type contributing most food
# ---------------------------
st.header("2️⃣ Provider Type Contribution")
type_contrib = listings.merge(providers, on="Provider_ID")
type_contrib = type_contrib.groupby("Type")["Quantity"].sum().sort_values(ascending=False)
st.bar_chart(type_contrib)

# ---------------------------
# Question 3: Contact info of providers in a city
# ---------------------------
st.header("3️⃣ Provider Contact Info by City")
selected_city = st.selectbox("Select City", sorted(providers["City"].unique()))
st.dataframe(providers[providers["City"] == selected_city][["Name", "Contact", "Email"]])

# ---------------------------
# Question 4: Receivers with most food claimed
# ---------------------------
st.header("4️⃣ Top Receivers by Claimed Food")
claims_completed = claims[claims["Status"].str.lower() == "completed"]
receiver_claims = claims_completed.groupby("Receiver_ID")["Quantity"].sum().reset_index()
receiver_claims = receiver_claims.merge(receivers, on="Receiver_ID")
st.dataframe(receiver_claims.sort_values("Quantity", ascending=False))

# ---------------------------
# Question 5: Total quantity of food available
# ---------------------------
st.header("5️⃣ Total Food Available")
total_food = listings["Quantity"].sum()
st.metric("Total Quantity Available", f"{total_food:,.0f}")

# ---------------------------
# Question 6: City with highest listings
# ---------------------------
st.header("6️⃣ City with Highest Food Listings")
city_listings = listings["Location"].value_counts()
st.bar_chart(city_listings)

# ---------------------------
# Question 7: Most common food types
# ---------------------------
st.header("7️⃣ Most Common Food Types")
food_types = listings["Food_Type"].value_counts()
st.bar_chart(food_types)

# ---------------------------
# Question 8: Claims per food item
# ---------------------------
st.header("8️⃣ Claims Made per Food Item")
food_claims = claims.merge(listings, on="Food_ID").groupby("Food_Name").size().sort_values(ascending=False)
st.dataframe(food_claims)

# ---------------------------
# Question 9: Provider with highest successful claims
# ---------------------------
st.header("9️⃣ Provider with Highest Successful Claims")
provider_success = claims_completed.merge(listings, on="Food_ID").merge(providers, on="Provider_ID")
provider_success = provider_success.groupby("Name").size().sort_values(ascending=False)
st.bar_chart(provider_success)

# ---------------------------
# Question 10: Percentage of claims by status
# ---------------------------
st.header("🔟 Claim Status Breakdown")
status_counts = claims["Status"].value_counts()
status_percent = (status_counts / status_counts.sum() * 100).round(2)
st.dataframe(pd.DataFrame({"Count": status_counts, "Percent": status_percent}))

# ---------------------------
# Question 11: Avg quantity claimed per receiver
# ---------------------------
st.header("1️⃣1️⃣ Average Quantity Claimed per Receiver")
avg_claims = claims_completed.groupby("Receiver_ID")["Quantity"].mean().reset_index()
avg_claims = avg_claims.merge(receivers, on="Receiver_ID")
st.dataframe(avg_claims.sort_values("Quantity", ascending=False))

# ---------------------------
# Question 12: Most claimed meal type
# ---------------------------
st.header("1️⃣2️⃣ Most Claimed Meal Type")
meal_claims = claims_completed.merge(listings, on="Food_ID").groupby("Meal_Type").size().sort_values(ascending=False)
st.bar_chart(meal_claims)

# ---------------------------
# Question 13: Total quantity donated by each provider
# ---------------------------
st.header("1️⃣3️⃣ Total Quantity Donated by Each Provider")
total_donated = listings.merge(providers, on="Provider_ID").groupby("Name")["Quantity"].sum().sort_values(ascending=False)
st.bar_chart(total_donated)

st.markdown("✅ Dashboard complete.")
