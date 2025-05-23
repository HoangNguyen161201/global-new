gif_paths = ['./public/gifs/gif_1.gif', './public/gifs/gif_2.gif', './public/gifs/gif_3.gif', './public/gifs/gif_4.gif']
person_img_paths = ['./public/persons/person_1.png', './public/persons/person_2.png', './public/persons/person_3.png', './public/persons/person_4.png']

edge_voice_data = [
    "en-US-AriaNeural",
    "en-US-AnaNeural",
    "en-US-ChristopherNeural",
    "en-US-EricNeural",
    "en-US-GuyNeural",
    "en-US-JennyNeural",
    "en-US-MichelleNeural",
    "en-US-RogerNeural",
    "en-US-SteffanNeural",
]




#  bạn hãy trả ra mảng như vầy,     { 
#         "content": "Make gelato, milkshakes, and more with the Ninja CREAMi Ice Cream Maker! Customize your flavors with ease. Check it out: https://amzn.to/4jn84aD",
#         "link_img": "https://f.media-amazon.com/images/I/71O-PzOILrL._AC_SL1500_.jpg",
#         "price": 200,
#         "discount": 13,
#         "link_item": "https://www.amazon.com/Ninja-NC301-placeholder-Cream-Maker/dp/B08QXB9BH5/ref=zg_mg_g_kitchen_d_sccl_22/141-6250380-7856552?th=1"
#     } content giưới thiệu sản phẩm không quá 120 ký tự, cố gắn giưới thiệu sao cho phù hợp với nhu cầu của người xem tin tức chính trị, hoặc nếu không thể được thì nêu công dụng trong content có chứa link affilicate



data_support = [
    {
        "content": "Crocs Classic Clogs, Comfortable shoes for everyday use. Shop now: https://amzn.to/4lJ7KVc",
        "link_img": "https://f.media-amazon.com/images/I/61SuPkDGYfL._AC_SY500_.jpg",
        "price": 37.99,
        "discount": 24,
        "link_item": "https://www.amazon.com/Crocs-Unisex-Classic-Black-Women/dp/B0014C2NBC/ref=zg_bs_c_fashion_d_sccl_2/141-6250380-7856552?pd_rd_w=QxANf&content-id=amzn1.sym.7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_p=7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_r=3G2C974ARBS64BXDZPYY&pd_rd_wg=A9qdA&pd_rd_r=d5149036-2913-475c-84c8-da0d40c49dfb&pd_rd_i=B0014C2NBC&psc=1"
    },
    {
        "content": "Stanley Quencher Tumbler, Keeps your drinks cold for hours. Get yours: https://amzn.to/4lJ3rZS",
        "link_img": "https://f.media-amazon.com/images/I/51SFVnJ-JWL._AC_SY879_.jpg",
        "price": 35,
        "discount": 0,
        "link_item": "https://www.amazon.com/Flowstate-3-Position-Compatible-Insulated-Stainless/dp/B0DR9PNXX3/ref=zg_bs_c_kitchen_d_sccl_1/141-6250380-7856552?pd_rd_w=nQznj&content-id=amzn1.sym.7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_p=7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_r=3G2C974ARBS64BXDZPYY&pd_rd_wg=A9qdA&pd_rd_r=d5149036-2913-475c-84c8-da0d40c49dfb&pd_rd_i=B0DR9PNXX3&th=1"
    },
    {
        "content": "EUHOMY Ice Maker, Make 26lbs of ice per day. Get one now: https://amzn.to/3S1DYxf",
        "link_img": "https://f.media-amazon.com/images/I/71GNZKaf+GL._AC_SX679_.jpg",
        "price": 89,
        "discount": 0,
        "link_item": "https://www.amazon.com/EUHOMY-Countertop-Machine-Auto-Cleaning-Portable/dp/B0BWHZJHPL/ref=zg_bs_g_appliances_d_sccl_1/141-6250380-7856552?th=1"
    },
    {
        "content": "Portable ice maker, makes 26 lbs of ice/day. Perfect for your kitchen or events: https://amzn.to/3Enr3Tk",
        "link_img": "https://f.media-amazon.com/images/I/61pVs0kk8EL._SX342_.jpg",
        "price": 69,
        "discount": 36,
        "link_item": "https://www.amazon.com/Silonn-Countertop-Portable-Machine-Self-Cleaning/dp/B0BXXKFJK2/ref=zg_bs_g_appliances_d_sccl_2/141-6250380-7856552?th=1"
    },
    {
        "content": "High performance microfiber towels, perfect for cleaning and car care: https://amzn.to/42YYxk4",
        "link_img": "https://f.media-amazon.com/images/I/A1U4ZA-OJmS._AC_SL1500_.jpg",
        "price": 8,
        "discount": 0,
        "link_item": "https://www.amazon.com/USANOOKS-Microfiber-Cleaning-Performance-Streak-Free/dp/B09FF4S39H/ref=zg_bs_g_appliances_d_sccl_2/141-6250380-7856552?th=1"
    },
    {
        "content": "Apple AirPods Pro 2 with active noise cancellation & spatial audio. Check it out: https://amzn.to/42sfByZ",
        "link_img": "https://f.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg",
        "price": 199,
        "discount": 20,
        "link_item": "https://www.amazon.com/Apple-Cancellation-Transparency-Personalized-High-Fidelity/dp/B0D1XD1ZV3/ref=zg_mw_c_electronics_d_sccl_2/141-6250380-7856552?pd_rd_w=7tHLz&content-id=amzn1.sym.7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_p=7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_r=BBQ2AWKQ4D04JW7CA7GR&pd_rd_wg=NzcNv&pd_rd_r=fa57012b-e917-439e-b077-a295f4ddde78&pd_rd_i=B0D1XD1ZV3&psc=1"
    },
    {
        "content": "Monitor your baby with the DoHonest Baby Car Camera. Safe and easy setup. See more: https://amzn.to/4cU52s4",
        "link_img": "https://f.media-amazon.com/images/I/71H0sRwiabL._SL1500_.jpg",
        "price": 24,
        "discount": 18,
        "link_item": "https://www.amazon.com/DoHonest-Baby-Camera-1080P-Display/dp/B0BRTSY1N9/ref=zg_mw_c_electronics_d_sccl_1/141-6250380-7856552?pd_rd_w=7tHLz&content-id=amzn1.sym.7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_p=7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_r=BBQ2AWKQ4D04JW7CA7GR&pd_rd_wg=NzcNv&pd_rd_r=fa57012b-e917-439e-b077-a295f4ddde78&pd_rd_i=B0BRTSY1N9&psc=1"
    },
    {
        "content": "With a vivid 11 display, the Amazon Fire Max 11 is perfect for all day entertainment and productivity: https://amzn.to/3EyGCHL",
        "link_img": "https://f.media-amazon.com/images/I/71wk6xXIzPL._AC_SL1500_.jpg",
        "price": 184,
        "discount": 20,
        "link_item": "https://www.amazon.com/Amazon-powerful-display-octa-core-processor/dp/B0B1VQ1ZQY/ref=zg_mg_g_pc_d_sccl_10/141-6250380-7856552?th=1"
    },
    {
        "content": "Boost productivity with the Anker USB C Hub, featuring 4K HDMI and fast charging: https://amzn.to/3YAfUp9",
        "link_img": "https://f.media-amazon.com/images/I/71u4FOC-AUL._AC_SL1500_.jpg",
        "price": 24,
        "discount": 29,
        "link_item": "https://www.amazon.com/Anker-Display-MacBook-Thinkpad-Laptops/dp/B0BQLLB61B/ref=zg_mg_g_pc_d_sccl_21/141-6250380-7856552?th=1"
    },
    {
        "content": "Protect your Kindle Paperwhite with this lightweight, water safe cover. Perfect for on the go reading. Check it out: https://amzn.to/447hTVk",
        "link_img": "https://f.media-amazon.com/images/I/71-KAuHFi+L._AC_SL1500_.jpg",
        "price": 36,
        "discount": 0,
        "link_item": "https://www.amazon.com/Amazon-Paperwhite-Lightweight-Water-Safe-Protective/dp/B0CM7X424T/ref=zg_mg_g_amazon-devices_d_sccl_3/141-6250380-7856552?th=1"
    },
    {
        "content": "Enjoy vibrant sound with the Amazon Echo Dot. A perfect addition to your home for music and Alexa assistance. Check it out: https://amzn.to/4iyFj9M",
        "link_img": "https://f.media-amazon.com/images/I/710exCeNPJL._AC_SL1000_.jpg",
        "price": 49,
        "discount": 0,
        "link_item": "https://www.amazon.com/Amazon-vibrant-helpful-routines-Charcoal/dp/B09B8V1LZ3/ref=zg_mg_g_amazon-devices_d_sccl_4/141-6250380-7856552?th=1"
    },
    {
        "content": "Get your day started with the Echo Spot Smart Alarm Clock. Wake up to music, check weather, and more. Check it out: https://amzn.to/3S0z2Zt",
        "link_img": "https://f.media-amazon.com/images/I/61Eu2owyKEL._AC_SL1000_.jpg",
        "price": 79,
        "discount": 0,
        "link_item": "https://www.amazon.com/All-new-Amazon-Echo-Spot-2024-release-Smart-alarm-clock-with-vibrant-sound-Alexa-Black/dp/B0BFC7WQ6R/ref=zg_mg_g_amazon-devices_d_sccl_12/141-6250380-7856552?th=1"
    },
    {
        "content": "Stay focused on reading without distractions with the Amazon Kindle Paperwhite. Perfect for those who need quiet time. Check it out: https://amzn.to/42G0VuP",
        "link_img": "https://f.media-amazon.com/images/I/719ws-Z0IyL._AC_SL1500_.jpg",
        "price": 159,
        "discount": 0,
        "link_item": "https://www.amazon.com/All-new-Amazon-Kindle-Paperwhite-glare-free/dp/B0CFPHV9ZN/ref=zg_mg_g_amazon-devices_d_sccl_13/141-6250380-7856552?th=1"
    },
    {
        "content": "Keep an eye on your home or business with the Ring Indoor Cam. Essential for safety and peace of mind. Check it out: https://amzn.to/3RxLsYG",
        "link_img": "https://f.media-amazon.com/images/I/51keHnu-7YL._SL1500_.jpg",
        "price": 34,
        "discount": 42,
        "link_item": "https://www.amazon.com/introducing-the-all-new-Ring-Indoor-Cam/dp/B0B6GLQJMV/ref=zg_mg_g_amazon-devices_d_sccl_23/141-6250380-7856552?th=1"
    },
    {
        "content": "Stay connected with the Apple iPhone 13, offering fast 5G downloads and a cinematic camera. A must have for staying in touch with the world. Check it out: https://amzn.to/3S3sGbM",
        "link_img": "https://f.media-amazon.com/images/I/51m4Ss9f3JL._AC_SL1000_.jpg",
        "price": 299,
        "discount": 0,
        "link_item": "https://www.amazon.com/Apple-iPhone-13-128GB-Red/dp/B0B5FGBLGY/ref=zg_mg_g_amazon-renewed_d_sccl_3/141-6250380-7856552?th=1"
    },
    {
        "content": "Stay productive with the Apple iPad 7th Gen. 32GB WiFi, perfect for reading news and multitasking. Check it out: https://amzn.to/3S3SkNy",
        "link_img": "https://f.media-amazon.com/images/I/61jCj1wN60L._AC_SL1265_.jpg",
        "price": 159,
        "discount": 10,
        "link_item": "https://www.amazon.com/Apple-iPad-10-2-Inch-Wi-Fi-32GB/dp/B0826562F1/ref=zg_mg_g_amazon-renewed_d_sccl_1/141-6250380-7856552?th=1"
    },
    {
        "content": "Track your health and stay connected with the Apple Watch Series 5. Perfect for staying on top of your day. Check it out: https://amzn.to/3YeC28h",
        "link_img": "https://f.media-amazon.com/images/I/71luYyAPVTL._AC_SL1500_.jpg",
        "price": 116,
        "discount": 0,
        "link_item": "https://www.amazon.com/Apple-Watch-GPS-40MM-Aluminum/dp/B083M6YZKT/ref=zg_mg_g_amazon-renewed_d_sccl_7/141-6250380-7856552?th=1"
    },
    {
        "content": "Experience the ultimate noise cancelling with Bose QuietComfort 45. Perfect for focused work or relaxation. Check it out: https://amzn.to/42JdZ2u",
        "link_img": "https://f.media-amazon.com/images/I/51Sb35c6-YL._AC_SL1148_.jpg",
        "price": 149,
        "discount": 54,
        "link_item": "https://www.amazon.com/Bose-QuietComfort-Bluetooth-Cancelling-Headphones/dp/B09HL9MQ64/ref=zg_mg_g_amazon-renewed_d_sccl_10/141-6250380-7856552?th=1"
    },
    {
        "content": "Stay focused on the news—block out noise with Dreamegg D11 Max: https://amzn.to/4cO0h36",
        "link_img": "https://f.media-amazon.com/images/I/71Il67Mwk-L._SL1500_.jpg",
        "price": 16.8,
        "discount": 30,
        "link_item": "https://www.amazon.com/Dreamegg-White-Noise-Machine-Canceling/dp/B0BBQX7P5J/ref=zg_mg_g_hpc_d_sccl_22/141-6250380-7856552?th=1"
    },
    {
        "content": "Block distractions and stay focused on world news with Momcozy: https://amzn.to/3S0oV6T",
        "link_img": "https://f.media-amazon.com/images/I/61YshwoMPJL._AC_SL1500_.jpg",
        "price": 36.5,
        "discount": 15,
        "link_item": "https://www.amazon.com/Machine-Momcozy-Sleeping-Soothing-Personal/dp/B0D5CYDF9T/ref=zg_mg_g_hpc_d_sccl_13/141-6250380-7856552?th=1"
    },
    {
        "content": "Whip up cookies, cakes, and more with ease using the KitchenAid 5 Speed Hand Mixer: https://amzn.to/3EvFVyY",
        "link_img": "https://f.media-amazon.com/images/I/71ivv1bvbhL._AC_SL1500_.jpg",
        "price": 60,
        "discount": 0,
        "link_item": "https://www.amazon.com/KitchenAid-KHM512AQ-Line-Speed-Mixer/dp/B07QCD9YS2/ref=zg_mg_g_kitchen_d_sccl_32/141-6250380-7856552?th=1"
    },
    {
        "content": "Stylish 16oz glass cup with bamboo lid & straw—perfect for iced drinks! A great gift idea. Check it out: https://amzn.to/3Rsu3AH",
        "link_img": "https://f.media-amazon.com/images/I/61DmLKMjh+L._AC_SL1500_.jpg",
        "price": 10,
        "discount": 0,
        "link_item": "https://www.amazon.com/Drinking-glasses-Aesthetics-Tumbler-Birthday/dp/B0D76FQQRH/ref=zg_mg_g_kitchen_d_sccl_26/141-6250380-7856552?th=1"
    },
    {
        "content": "Make gelato, milkshakes, and more with the Ninja CREAMi Ice Cream Maker! Customize your flavors with ease. Check it out: https://amzn.to/4jn84aD",
        "link_img": "https://f.media-amazon.com/images/I/71O-PzOILrL._AC_SL1500_.jpg",
        "price": 200,
        "discount": 13,
        "link_item": "https://www.amazon.com/Ninja-NC301-placeholder-Cream-Maker/dp/B08QXB9BH5/ref=zg_mg_g_kitchen_d_sccl_22/141-6250380-7856552?th=1"
    },
    { 
        "content": "Protect your baby from UV rays with this Monobeach Baby Beach Tent! Ideal for beach trips. Check it out: https://amzn.to/4ivEMWa", 
        "link_img": "https://f.media-amazon.com/images/I/6103YlWQqoS._AC_SL1500_.jpg", 
        "price": 29.7, 
        "discount": 41, 
        "link_item": "https://www.amazon.com/Monobeach-Portable-Protection-Shelter-Infant/dp/B01K15UQ4I/ref=zg_mg_g_sporting-goods_d_sccl_32/141-6250380-7856552?th=1"
    },
    { 
        "content": "Track your health and manage stress with the Fitbit Inspire 3 Fitness Tracker. Keep active & relaxed! Check it out: https://amzn.to/3S0AU4r", 
        "link_img": "https://f.media-amazon.com/images/I/51aGiZ-UJ-L._AC_SL1200_.jpg", 
        "price": 99.95, 
        "discount": 0, 
        "link_item": "https://www.amazon.com/Fitbit-Management-Intensity-Tracking-Included/dp/B0B5FCYMFD/ref=zg_mg_g_sporting-goods_d_sccl_36/141-6250380-7856552?th=1"
    },
    { 
        "content": "Boost your child's balance and coordination with the Micro Mini Deluxe Scooter. Durable and fun! Check it out: https://amzn.to/4iqjoRR", 
        "link_img": "https://f.media-amazon.com/images/I/71YWicteDKL._AC_SL1500_.jpg", 
        "price": 90, 
        "discount": 0, 
        "link_item": "https://www.amazon.com/Micro-Mini-Deluxe-Scooter-Blue/dp/B01BE0JGE0/ref=zg_mg_g_sporting-goods_d_sccl_42/141-6250380-7856552?th=1"
    },
    { 
        "content": "Decorate your room with vibrant LED lights. Sync them to music and create an immersive atmosphere! Check it out: https://amzn.to/3RstDu7", 
        "link_img": "https://f.media-amazon.com/images/I/81cEqfpA5+L._AC_SL1500_.jpg", 
        "price": 14, 
        "discount": 0, 
        "link_item": "https://www.amazon.com/Daybetter-Lights-Control-Bedroom-Changing/dp/B08JSFH1G6/ref=zg_mg_g_hi_d_sccl_13/141-6250380-7856552?th=1"
    },
    { 
        "content": "Help your toddler develop balance with the SEREED Baby Balance Bike. Safe and sturdy for first time riders. Check it out: https://amzn.to/4jnzKMH", 
        "link_img": "https://f.media-amazon.com/images/I/61EKfoSmrUL._AC_SL1500_.jpg", 
        "price": 44, 
        "discount": 10, 
        "link_item": "https://www.amazon.com/SEREED-Balance-Months-Toddler-Birthday/dp/B0BVJ1KL96/ref=zg_mg_g_toys-and-games_d_sccl_3/141-6250380-7856552?th=1"
    },
    
    {
        "content": "Keep your phone steady while driving with this versatile 3 in 1 car mount. Check it out: https://amzn.to/42Hdcz3",
        "link_img": "https://f.media-amazon.com/images/I/91Yg33Uoc6L._AC_SL1500_.jpg",
        "price": 33,
        "discount": 9,
        "link_item": "https://www.amazon.com/Qifutan-Windshield-Dashboard-Automobile-Smartphone/dp/B0CHS69JW3/ref=zg_mg_g_automotive_d_sccl_19/141-6250380-7856552?th=1"
    },
    {
        "content": "Keep your car organized and your kids entertained with this backseat organizer. Perfect for long drives. Check it out: https://amzn.to/42MJ2up",
        "link_img": "https://f.media-amazon.com/images/I/91WpBQ+nZGL._AC_SL1500_.jpg",
        "price": 25,
        "discount": 0,
        "link_item": "https://www.amazon.com/Helteko-Backseat-Car-Organizer-Accessories/dp/B07RNZV64Y/ref=zg_mg_g_automotive_d_sccl_29/141-6250380-7856552?th=1"
    },
    {
        "content": "Stay in shape with these durable neoprene dumbbells. Ideal for home workouts. Check them out: https://amzn.to/446UHqq",
        "link_img": "https://f.media-amazon.com/images/I/51jdrkKXWEL._AC_SL1269_.jpg",
        "price": 6.5,
        "discount": 0,
        "link_item": "https://www.amazon.com/AmazonBasics-Pound-Neoprene-Dumbbells-Weights/dp/B01LR5R18K/ref=zg_mg_g_sporting-goods_d_sccl_8/141-6250380-7856552?th=1"
    },
    {
        "content": "Protect your kids with this adjustable bike helmet for safe outdoor fun. Check it out: https://amzn.to/4iugw6D",
        "link_img": "https://f.media-amazon.com/images/I/61p4j8faB3L._AC_SL1500_.jpg",
        "price": 33,
        "discount": 11,
        "link_item": "https://www.amazon.com/Ouwoer-Certified-Adjustable-Multi-Sport-Toddler/dp/B07CXL2NCT/ref=zg_mg_g_sporting-goods_d_sccl_20/141-6250380-7856552?th=1"
    },
    
    {
        "content": "2021 Apple iPad, Perfect for staying updated on the latest political news. Check it out: https://amzn.to/3YHs0N0",
        "link_img": "https://f.media-amazon.com/images/I/61fbS-pklLL._AC_SL1500_.jpg",
        "price": 219,
        "discount": 31,
        "link_item": "https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09HV3D2SX/ref=zg_mg_g_amazon-renewed_d_sccl_24/141-6250380-7856552?th=1"
    },
    {
        "content": "Shark Steam Mop Keep your floors clean. Check it out: https://amzn.to/3YfnGVc",
        "link_img": "https://f.media-amazon.com/images/I/51Al8dUI5XL._AC_SL1383_.jpg",
        "price": 80,
        "discount": 0,
        "link_item": "https://www.amazon.com/Professional-Super-Heated-Pocket-Certified-Refurbished/dp/B01JZMMUEW/ref=zg_mg_g_amazon-renewed_d_sccl_29/141-6250380-7856552?psc=1"
    },
    {
        "content": "Samsung Galaxy Watch 6, Monitor your health while staying connected to breaking news. Check it out: https://amzn.to/3RvtVAo",
        "link_img": "https://f.media-amazon.com/images/I/51zBhMSh0uL._AC_SL1000_.jpg",
        "price": 79.43,
        "discount": 41,
        "link_item": "https://www.amazon.com/Samsung-Smartwatch-Rotating-Advanced-Coaching/dp/B0CVLJNPQG/ref=zg_mg_g_amazon-renewed_d_sccl_34/141-6250380-7856552?th=1"
    },
    {
        "content": "Ninja Cold Press Juicer, Enjoy fresh juices while keeping up with current events. Check it out: https://amzn.to/3EmKR9n",
        "link_img": "https://f.media-amazon.com/images/I/71UY-8c6GVL._AC_SL1500_.jpg",
        "price": 89,
        "discount": 32,
        "link_item": "https://www.amazon.com/Ninja-NeverClog-Countertop-Dishwasher-Generation/dp/B0CKGNZH2K/ref=zg_mg_g_amazon-renewed_d_sccl_22/141-6250380-7856552?psc=1"
    },
    {
        "content": "JBL Flip 5 Speaker, Keep the music flowing. Check it out: https://amzn.to/3ElvIoP",
        "link_img": "https://f.media-amazon.com/images/I/71cOhRozhFL._AC_SL1500_.jpg",
        "price": 79.97,
        "discount": 11,
        "link_item": "https://www.amazon.com/JBL-Portable-Waterproof-Wireless-Bluetooth/dp/B08BF54PB1/ref=zg_mg_g_amazon-renewed_d_sccl_25/141-6250380-7856552?th=1"
    },
    {
    "content": "Enjoy high quality sound with Beats Studio3 Wireless Headphones! Perfect for music lovers. Check it out: https://amzn.to/4cGgS8O",
    "link_img": "https://f.media-amazon.com/images/I/51MEFehsDaL._AC_SL1500_.jpg",
    "price": 114,
    "discount": 32,
    "link_item": "https://www.amazon.com/Beats-Studio3-Wireless-Headphones-Renewed/dp/B079TLV1WW/ref=zg_mg_g_amazon-renewed_d_sccl_14/141-6250380-7856552?th=1"
    }
]

print(data_support.__len__())


