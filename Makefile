MODULES = discord requests pytz pyttsx3 yt-dlp imageio translatepy gtts rembg onnxruntime PyNaCl

.PHONY: all

all: dependencies assets_files install

dependencies:
	pip3 install $(MODULES)

assets_files:
	mkdir assets 
	mkdir assets/images
	mkdir assets/tiktok
	mkdir assets/yt
	touch assets/admins.log
	touch assets/blacklist_join.log
	touch assets/blacklisted_token.log
	touch assets/deleted.log
	touch assets/skids.log