#!/bin/sh

LOCAL_PATH=$(pwd)
NEW_NAVBAR_HEIGHT=$2
APKTOOL="$LOCAL_PATH/apktool.jar"

FOLDER_TMP="$LOCAL_PATH/tmp"
FOLDER_OUT="$LOCAL_PATH/out"
FOLDER_DECOMPILE="$FOLDER_TMP/framework-res-edit"
FOLDER_EXTRACTED="$FOLDER_TMP/framework-extracted"

FILE_BOOLS="$FOLDER_DECOMPILE/res/values/bools.xml"
FILE_DIMENS="$FOLDER_DECOMPILE/res/values/dimens.xml"

FRAMEWORK_ORIGINAL=$1
FRAMEWORK_NEW="$FOLDER_OUT/framework-res.apk"

showusage() {
  echo -e "Usage: $0 framework-res.apk [navigation_bar_height]\n"
}

if [ ! -f "$FRAMEWORK_ORIGINAL" ];then
  if [ -z "$FRAMEWORK_ORIGINAL" ];then
    showusage
  else
    echo "ERROR: File '$FRAMEWORK_ORIGINAL' not found!"
  fi
  
  exit 1
fi

echo "Cleanup ..."
rm -Rf $FOLDER_TMP
rm -Rf $FOLDER_OUT
mkdir -p $FOLDER_TMP
mkdir -p $FOLDER_OUT

echo "Decompile '$FRAMEWORK_ORIGINAL' ..."
java -jar $APKTOOL d $FRAMEWORK_ORIGINAL $FOLDER_DECOMPILE

echo "Enable Navigationbar ..."
sed -i 's/<bool name=config_showNavigationBar>false<\/bool>/<bool name=config_showNavigationBar>true<\/bool>/g' $FILE_BOOLS
sed -i 's/<bool name="config_showNavigationBar">false<\/bool>/<bool name="config_showNavigationBar">true<\/bool>/g' $FILE_BOOLS

if [ -n "$NEW_NAVBAR_HEIGHT" ];then
  echo "Set Navigationbar height to '$NEW_NAVBAR_HEIGHT' ..."
  sed -i "s/<dimen name=navigation_bar_height>.*<\/dimen>/<dimen name=navigation_bar_height>$NEW_NAVBAR_HEIGHT<\/dimen>/g" $FILE_DIMENS
  sed -i "s/<dimen name=\"navigation_bar_height\">.*<\/dimen>/<dimen name=\"navigation_bar_height\">$NEW_NAVBAR_HEIGHT<\/dimen>/g" $FILE_DIMENS
fi

echo "Recompile ..."
java -jar $APKTOOL b $FOLDER_DECOMPILE

echo "Build final framework ..."
cp "$FRAMEWORK_ORIGINAL" "$FRAMEWORK_NEW"
cd "$FOLDER_DECOMPILE/build/apk"
zip -r "$FRAMEWORK_NEW" ./res
zip -0 "$FRAMEWORK_NEW" ./resources.arsc

echo "Done."
echo "Patched file: $FRAMEWORK_NEW"