Unicode true
Name "Qimat"
OutFile "dist\Qimat_v1_2_2_Setup_Windows7Plus.exe"
InstallDir "$LOCALAPPDATA\Programs\Qimat"
RequestExecutionLevel user
SetCompressor /SOLID lzma

VIProductVersion "1.2.2.0"
VIAddVersionKey "ProductName" "Qimat"
VIAddVersionKey "FileDescription" "Qimat Setup"
VIAddVersionKey "FileVersion" "1.2.2"
VIAddVersionKey "ProductVersion" "1.2.2"

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Qimat" SEC_MAIN
  SetOutPath "$INSTDIR"
  File "dist\Qimat_v1_2_2_Windows7Plus.exe"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\Qimat"
  CreateShortcut "$SMPROGRAMS\Qimat\Qimat.lnk" "$INSTDIR\Qimat_v1_2_2_Windows7Plus.exe"
  CreateShortcut "$DESKTOP\Qimat.lnk" "$INSTDIR\Qimat_v1_2_2_Windows7Plus.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\Qimat.lnk"
  Delete "$SMPROGRAMS\Qimat\Qimat.lnk"
  RMDir "$SMPROGRAMS\Qimat"
  Delete "$INSTDIR\Qimat_v1_2_2_Windows7Plus.exe"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  ; اطلاعات ثبت‌شده کاربر عمداً حذف نمی‌شود.
SectionEnd
