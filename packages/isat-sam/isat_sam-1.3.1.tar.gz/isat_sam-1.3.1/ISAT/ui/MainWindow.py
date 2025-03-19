# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/lg/disk2/PycharmProjects/ISAT_with_segment_anything/ISAT/ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icons/ISAT13_100.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menubar.setFont(font)
        self.menubar.setAutoFillBackground(False)
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuView.setFont(font)
        self.menuView.setObjectName("menuView")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuAbout.setFont(font)
        self.menuAbout.setObjectName("menuAbout")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuTools.setFont(font)
        self.menuTools.setObjectName("menuTools")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuEdit.setFont(font)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSAM_model = QtWidgets.QMenu(self.menubar)
        self.menuSAM_model.setObjectName("menuSAM_model")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.toolBar.setFont(font)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.info_dock = QtWidgets.QDockWidget(MainWindow)
        self.info_dock.setMinimumSize(QtCore.QSize(85, 43))
        self.info_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.info_dock.setObjectName("info_dock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.info_dock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.info_dock)
        self.annos_dock = QtWidgets.QDockWidget(MainWindow)
        self.annos_dock.setMinimumSize(QtCore.QSize(85, 43))
        self.annos_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.annos_dock.setObjectName("annos_dock")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.annos_dock.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.annos_dock)
        self.files_dock = QtWidgets.QDockWidget(MainWindow)
        self.files_dock.setObjectName("files_dock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.files_dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.files_dock)
        self.categories_dock = QtWidgets.QDockWidget(MainWindow)
        self.categories_dock.setObjectName("categories_dock")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.categories_dock.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.categories_dock)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setMovable(False)
        self.toolBar_2.setFloatable(False)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar_2)
        self.actionImages_dir = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icons/照片_pic.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImages_dir.setIcon(icon1)
        self.actionImages_dir.setObjectName("actionImages_dir")
        self.actionZoom_in = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icons/放大_zoom-in.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_in.setIcon(icon2)
        self.actionZoom_in.setObjectName("actionZoom_in")
        self.actionZoom_out = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icons/缩小_zoom-out.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon3)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.actionFit_window = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/icons/全宽_fullwidth.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFit_window.setIcon(icon4)
        self.actionFit_window.setObjectName("actionFit_window")
        self.actionSetting = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/icons/设置_setting-two.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetting.setIcon(icon5)
        self.actionSetting.setObjectName("actionSetting")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/icons/开关_power.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon6)
        self.actionExit.setObjectName("actionExit")
        self.actionLabel_dir = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/icons/文件夹-开_folder-open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLabel_dir.setIcon(icon7)
        self.actionLabel_dir.setObjectName("actionLabel_dir")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icon/icons/保存_save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionPrev_image = QtWidgets.QAction(MainWindow)
        self.actionPrev_image.setCheckable(False)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icon/icons/上一步_back.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev_image.setIcon(icon9)
        self.actionPrev_image.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionPrev_image.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionPrev_image.setObjectName("actionPrev_image")
        self.actionNext_image = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icon/icons/下一步_next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext_image.setIcon(icon10)
        self.actionNext_image.setObjectName("actionNext_image")
        self.actionShortcut = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icon/icons/键盘_keyboard-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShortcut.setIcon(icon11)
        self.actionShortcut.setObjectName("actionShortcut")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icon/icons/ISAT13.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon12)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSegment_anything_point = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icon/icons/M_Favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSegment_anything_point.setIcon(icon13)
        self.actionSegment_anything_point.setObjectName("actionSegment_anything_point")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setEnabled(False)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icon/icons/删除_delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon14)
        self.actionDelete.setObjectName("actionDelete")
        self.actionBit_map = QtWidgets.QAction(MainWindow)
        self.actionBit_map.setCheckable(False)
        self.actionBit_map.setIcon(icon1)
        self.actionBit_map.setObjectName("actionBit_map")
        self.actionEdit = QtWidgets.QAction(MainWindow)
        self.actionEdit.setEnabled(False)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icon/icons/编辑_edit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon15)
        self.actionEdit.setObjectName("actionEdit")
        self.actionTo_top = QtWidgets.QAction(MainWindow)
        self.actionTo_top.setEnabled(False)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icon/icons/去顶部_to-top.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTo_top.setIcon(icon16)
        self.actionTo_top.setObjectName("actionTo_top")
        self.actionTo_bottom = QtWidgets.QAction(MainWindow)
        self.actionTo_bottom.setEnabled(False)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icon/icons/去底部_to-bottom.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTo_bottom.setIcon(icon17)
        self.actionTo_bottom.setObjectName("actionTo_bottom")
        self.actionBackspace = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icon/icons/删除_delete-two.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackspace.setIcon(icon18)
        self.actionBackspace.setObjectName("actionBackspace")
        self.actionCancel = QtWidgets.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/icon/icons/关闭_close-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon19)
        self.actionCancel.setObjectName("actionCancel")
        self.actionFinish = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/icon/icons/校验_check-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFinish.setIcon(icon20)
        self.actionFinish.setObjectName("actionFinish")
        self.actionPolygon = QtWidgets.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/icon/icons/锚点_anchor.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPolygon.setIcon(icon21)
        self.actionPolygon.setObjectName("actionPolygon")
        self.actionVisible = QtWidgets.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/icon/icons/眼睛_eyes.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVisible.setIcon(icon22)
        self.actionVisible.setObjectName("actionVisible")
        self.actionModel_manage = QtWidgets.QAction(MainWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/icon/icons/列表_list-middle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionModel_manage.setIcon(icon23)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionModel_manage.setFont(font)
        self.actionModel_manage.setObjectName("actionModel_manage")
        self.actionConverter = QtWidgets.QAction(MainWindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/icon/icons/转换文件夹1_folder-conversion-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConverter.setIcon(icon24)
        self.actionConverter.setObjectName("actionConverter")
        self.actionAuto_segment_with_bounding_box = QtWidgets.QAction(MainWindow)
        self.actionAuto_segment_with_bounding_box.setIcon(icon13)
        self.actionAuto_segment_with_bounding_box.setObjectName("actionAuto_segment_with_bounding_box")
        self.actionAnno_validator = QtWidgets.QAction(MainWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/icon/icons/检查_inspection.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAnno_validator.setIcon(icon25)
        self.actionAnno_validator.setObjectName("actionAnno_validator")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(":/icon/icons/复制_copy.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon26)
        self.actionCopy.setObjectName("actionCopy")
        self.actionUnion = QtWidgets.QAction(MainWindow)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(":/icon/icons/合并选择_union-selection.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUnion.setIcon(icon27)
        self.actionUnion.setObjectName("actionUnion")
        self.actionSubtract = QtWidgets.QAction(MainWindow)
        icon28 = QtGui.QIcon()
        icon28.addPixmap(QtGui.QPixmap(":/icon/icons/减去上一层_subtract-selection-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSubtract.setIcon(icon28)
        self.actionSubtract.setObjectName("actionSubtract")
        self.actionIntersect = QtWidgets.QAction(MainWindow)
        icon29 = QtGui.QIcon()
        icon29.addPixmap(QtGui.QPixmap(":/icon/icons/相交选择_intersect-selection.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIntersect.setIcon(icon29)
        self.actionIntersect.setObjectName("actionIntersect")
        self.actionExclude = QtWidgets.QAction(MainWindow)
        icon30 = QtGui.QIcon()
        icon30.addPixmap(QtGui.QPixmap(":/icon/icons/排除选择_exclude-selection.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExclude.setIcon(icon30)
        self.actionExclude.setObjectName("actionExclude")
        self.actionVideo_segment = QtWidgets.QAction(MainWindow)
        icon31 = QtGui.QIcon()
        icon31.addPixmap(QtGui.QPixmap(":/icon/icons/play-all.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVideo_segment.setIcon(icon31)
        self.actionVideo_segment.setObjectName("actionVideo_segment")
        self.actionVideo_segment_once = QtWidgets.QAction(MainWindow)
        icon32 = QtGui.QIcon()
        icon32.addPixmap(QtGui.QPixmap(":/icon/icons/play-1.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVideo_segment_once.setIcon(icon32)
        self.actionVideo_segment_once.setObjectName("actionVideo_segment_once")
        self.actionVideo_segment_five_times = QtWidgets.QAction(MainWindow)
        icon33 = QtGui.QIcon()
        icon33.addPixmap(QtGui.QPixmap(":/icon/icons/play-5.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVideo_segment_five_times.setIcon(icon33)
        self.actionVideo_segment_five_times.setObjectName("actionVideo_segment_five_times")
        self.actionVideo_to_frames = QtWidgets.QAction(MainWindow)
        icon34 = QtGui.QIcon()
        icon34.addPixmap(QtGui.QPixmap(":/icon/icons/视频_video-two.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVideo_to_frames.setIcon(icon34)
        self.actionVideo_to_frames.setObjectName("actionVideo_to_frames")
        self.actionSegment_anything_box = QtWidgets.QAction(MainWindow)
        icon35 = QtGui.QIcon()
        icon35.addPixmap(QtGui.QPixmap(":/icon/icons/小矩形_rectangle-small.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSegment_anything_box.setIcon(icon35)
        self.actionSegment_anything_box.setObjectName("actionSegment_anything_box")
        self.actionPrev_group = QtWidgets.QAction(MainWindow)
        self.actionPrev_group.setIcon(icon9)
        self.actionPrev_group.setObjectName("actionPrev_group")
        self.actionNext_group = QtWidgets.QAction(MainWindow)
        self.actionNext_group.setIcon(icon10)
        self.actionNext_group.setObjectName("actionNext_group")
        self.actionRepaint = QtWidgets.QAction(MainWindow)
        icon36 = QtGui.QIcon()
        icon36.addPixmap(QtGui.QPixmap(":/icon/icons/编辑撰写_writing-fluently.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRepaint.setIcon(icon36)
        self.actionRepaint.setObjectName("actionRepaint")
        self.actionScene_shot = QtWidgets.QAction(MainWindow)
        icon37 = QtGui.QIcon()
        icon37.addPixmap(QtGui.QPixmap(":/icon/icons/截屏_screenshot-two.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionScene_shot.setIcon(icon37)
        self.actionScene_shot.setObjectName("actionScene_shot")
        self.actionWindow_shot = QtWidgets.QAction(MainWindow)
        self.actionWindow_shot.setIcon(icon37)
        self.actionWindow_shot.setObjectName("actionWindow_shot")
        self.actionLanguage = QtWidgets.QAction(MainWindow)
        icon38 = QtGui.QIcon()
        icon38.addPixmap(QtGui.QPixmap(":/icon/icons/中文_chinese.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLanguage.setIcon(icon38)
        self.actionLanguage.setObjectName("actionLanguage")
        self.menuFile.addAction(self.actionImages_dir)
        self.menuFile.addAction(self.actionLabel_dir)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrev_image)
        self.menuFile.addAction(self.actionNext_image)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSetting)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionPrev_group)
        self.menuView.addAction(self.actionNext_group)
        self.menuView.addAction(self.actionVisible)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionBit_map)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoom_in)
        self.menuView.addAction(self.actionZoom_out)
        self.menuView.addAction(self.actionFit_window)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionScene_shot)
        self.menuView.addAction(self.actionWindow_shot)
        self.menuAbout.addAction(self.actionLanguage)
        self.menuAbout.addAction(self.actionShortcut)
        self.menuAbout.addAction(self.actionAbout)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionConverter)
        self.menuTools.addAction(self.actionVideo_to_frames)
        self.menuTools.addAction(self.actionAuto_segment_with_bounding_box)
        self.menuTools.addAction(self.actionAnno_validator)
        self.menuEdit.addAction(self.actionSegment_anything_point)
        self.menuEdit.addAction(self.actionSegment_anything_box)
        self.menuEdit.addAction(self.actionPolygon)
        self.menuEdit.addAction(self.actionRepaint)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionVideo_segment)
        self.menuEdit.addAction(self.actionVideo_segment_once)
        self.menuEdit.addAction(self.actionVideo_segment_five_times)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionBackspace)
        self.menuEdit.addAction(self.actionFinish)
        self.menuEdit.addAction(self.actionCancel)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEdit)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionTo_top)
        self.menuEdit.addAction(self.actionTo_bottom)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUnion)
        self.menuEdit.addAction(self.actionSubtract)
        self.menuEdit.addAction(self.actionIntersect)
        self.menuEdit.addAction(self.actionExclude)
        self.menuSAM_model.addAction(self.actionModel_manage)
        self.menuSAM_model.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSAM_model.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionPrev_image)
        self.toolBar.addAction(self.actionNext_image)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSegment_anything_point)
        self.toolBar.addAction(self.actionSegment_anything_box)
        self.toolBar.addAction(self.actionPolygon)
        self.toolBar.addAction(self.actionRepaint)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionVideo_segment_once)
        self.toolBar.addAction(self.actionVideo_segment_five_times)
        self.toolBar.addAction(self.actionVideo_segment)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionBackspace)
        self.toolBar.addAction(self.actionFinish)
        self.toolBar.addAction(self.actionCancel)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTo_top)
        self.toolBar.addAction(self.actionTo_bottom)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUnion)
        self.toolBar.addAction(self.actionSubtract)
        self.toolBar.addAction(self.actionIntersect)
        self.toolBar.addAction(self.actionExclude)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoom_in)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionFit_window)
        self.toolBar.addAction(self.actionBit_map)
        self.toolBar.addAction(self.actionVisible)
        self.toolBar_2.addAction(self.actionModel_manage)
        self.toolBar_2.addAction(self.actionShortcut)
        self.toolBar_2.addAction(self.actionSetting)
        self.toolBar_2.addAction(self.actionLanguage)
        self.toolBar_2.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ISAT"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuSAM_model.setTitle(_translate("MainWindow", "SAM"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.info_dock.setWindowTitle(_translate("MainWindow", "Info"))
        self.annos_dock.setWindowTitle(_translate("MainWindow", "Annos"))
        self.files_dock.setWindowTitle(_translate("MainWindow", "Files"))
        self.categories_dock.setWindowTitle(_translate("MainWindow", "Categories"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.actionImages_dir.setText(_translate("MainWindow", "Images dir"))
        self.actionImages_dir.setStatusTip(_translate("MainWindow", "Open images dir."))
        self.actionZoom_in.setText(_translate("MainWindow", "Zoom in"))
        self.actionZoom_in.setStatusTip(_translate("MainWindow", "Zoom in."))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out"))
        self.actionZoom_out.setStatusTip(_translate("MainWindow", "Zoom out."))
        self.actionFit_window.setText(_translate("MainWindow", "Fit window"))
        self.actionFit_window.setToolTip(_translate("MainWindow", "Fit window"))
        self.actionFit_window.setStatusTip(_translate("MainWindow", "Fit window."))
        self.actionFit_window.setShortcut(_translate("MainWindow", "F"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionSetting.setStatusTip(_translate("MainWindow", "Setting."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit."))
        self.actionLabel_dir.setText(_translate("MainWindow", "Label dir"))
        self.actionLabel_dir.setStatusTip(_translate("MainWindow", "Open label dir."))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save annotation."))
        self.actionSave.setShortcut(_translate("MainWindow", "S"))
        self.actionPrev_image.setText(_translate("MainWindow", "Prev image"))
        self.actionPrev_image.setToolTip(_translate("MainWindow", "Prev image"))
        self.actionPrev_image.setStatusTip(_translate("MainWindow", "Prev image."))
        self.actionPrev_image.setShortcut(_translate("MainWindow", "A"))
        self.actionNext_image.setText(_translate("MainWindow", "Next image"))
        self.actionNext_image.setToolTip(_translate("MainWindow", "Next image"))
        self.actionNext_image.setStatusTip(_translate("MainWindow", "Next image."))
        self.actionNext_image.setShortcut(_translate("MainWindow", "D"))
        self.actionShortcut.setText(_translate("MainWindow", "Shortcut"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSegment_anything_point.setText(_translate("MainWindow", "Segment anything point"))
        self.actionSegment_anything_point.setToolTip(_translate("MainWindow", "Segment anything point"))
        self.actionSegment_anything_point.setStatusTip(_translate("MainWindow", "Quick annotate using Segment anything."))
        self.actionSegment_anything_point.setShortcut(_translate("MainWindow", "Q"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setToolTip(_translate("MainWindow", "Delete polygon"))
        self.actionDelete.setStatusTip(_translate("MainWindow", "Delete polygon."))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionBit_map.setText(_translate("MainWindow", "Bit map"))
        self.actionBit_map.setStatusTip(_translate("MainWindow", "Show instance or segmeent state."))
        self.actionBit_map.setShortcut(_translate("MainWindow", "Space"))
        self.actionEdit.setText(_translate("MainWindow", "Edit"))
        self.actionEdit.setToolTip(_translate("MainWindow", "Edit polygon"))
        self.actionEdit.setStatusTip(_translate("MainWindow", "Edit polygon attribute."))
        self.actionTo_top.setText(_translate("MainWindow", "To top"))
        self.actionTo_top.setToolTip(_translate("MainWindow", "Move polygon to top layer"))
        self.actionTo_top.setStatusTip(_translate("MainWindow", "Move polygon to top layer."))
        self.actionTo_top.setShortcut(_translate("MainWindow", "T"))
        self.actionTo_bottom.setText(_translate("MainWindow", "To bottom"))
        self.actionTo_bottom.setToolTip(_translate("MainWindow", "Move polygon to bottom layer"))
        self.actionTo_bottom.setStatusTip(_translate("MainWindow", "Move polygon to bottom layer."))
        self.actionTo_bottom.setShortcut(_translate("MainWindow", "B"))
        self.actionBackspace.setText(_translate("MainWindow", "Backspace"))
        self.actionBackspace.setToolTip(_translate("MainWindow", "Backspace"))
        self.actionBackspace.setStatusTip(_translate("MainWindow", "Backspace."))
        self.actionBackspace.setShortcut(_translate("MainWindow", "Z"))
        self.actionCancel.setText(_translate("MainWindow", "Cancel"))
        self.actionCancel.setToolTip(_translate("MainWindow", "Annotate canceled"))
        self.actionCancel.setStatusTip(_translate("MainWindow", "Annotate canceled."))
        self.actionCancel.setShortcut(_translate("MainWindow", "Esc"))
        self.actionFinish.setText(_translate("MainWindow", "Finish"))
        self.actionFinish.setToolTip(_translate("MainWindow", "Annotate finished"))
        self.actionFinish.setStatusTip(_translate("MainWindow", "Annotate finished."))
        self.actionFinish.setShortcut(_translate("MainWindow", "E"))
        self.actionPolygon.setText(_translate("MainWindow", "Polygon"))
        self.actionPolygon.setToolTip(_translate("MainWindow", "Draw polygon"))
        self.actionPolygon.setStatusTip(_translate("MainWindow", "Accurately annotate by drawing polygon. "))
        self.actionPolygon.setShortcut(_translate("MainWindow", "C"))
        self.actionVisible.setText(_translate("MainWindow", "Visible"))
        self.actionVisible.setToolTip(_translate("MainWindow", "Visible"))
        self.actionVisible.setStatusTip(_translate("MainWindow", "Visible."))
        self.actionVisible.setShortcut(_translate("MainWindow", "V"))
        self.actionModel_manage.setText(_translate("MainWindow", "Model manage"))
        self.actionModel_manage.setStatusTip(_translate("MainWindow", "Model manage."))
        self.actionModel_manage.setWhatsThis(_translate("MainWindow", "Model manage."))
        self.actionConverter.setText(_translate("MainWindow", "Converter"))
        self.actionAuto_segment_with_bounding_box.setText(_translate("MainWindow", "Auto segment with bounding box"))
        self.actionAnno_validator.setText(_translate("MainWindow", "Annos validator"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionUnion.setText(_translate("MainWindow", "Union"))
        self.actionUnion.setStatusTip(_translate("MainWindow", "Select two polygons from the canvas and calculate their union. "))
        self.actionUnion.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionSubtract.setText(_translate("MainWindow", "Subtract"))
        self.actionSubtract.setStatusTip(_translate("MainWindow", "Select two polygons from the canvas and calculate their subtract. "))
        self.actionSubtract.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionIntersect.setText(_translate("MainWindow", "Intersect"))
        self.actionIntersect.setStatusTip(_translate("MainWindow", "Select two polygons from the canvas and calculate their intersect. "))
        self.actionIntersect.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionExclude.setText(_translate("MainWindow", "Exclude"))
        self.actionExclude.setStatusTip(_translate("MainWindow", "Select two polygons from the canvas and calculate their exclude. "))
        self.actionExclude.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionVideo_segment.setText(_translate("MainWindow", "Video segment"))
        self.actionVideo_segment.setStatusTip(_translate("MainWindow", "Video segment full frames.(only support sam2 model)"))
        self.actionVideo_segment_once.setText(_translate("MainWindow", "Video segment once"))
        self.actionVideo_segment_once.setStatusTip(_translate("MainWindow", "Video segment the next frame.(only support sam2 model)"))
        self.actionVideo_segment_five_times.setText(_translate("MainWindow", "Video segment five times"))
        self.actionVideo_segment_five_times.setStatusTip(_translate("MainWindow", "Video segment next five frames.(only support sam2 model)"))
        self.actionVideo_to_frames.setText(_translate("MainWindow", "Video to frames"))
        self.actionSegment_anything_box.setText(_translate("MainWindow", "Segment anything box"))
        self.actionSegment_anything_box.setStatusTip(_translate("MainWindow", "Quick annotate using Segment anything."))
        self.actionSegment_anything_box.setShortcut(_translate("MainWindow", "W"))
        self.actionPrev_group.setText(_translate("MainWindow", "Prev group"))
        self.actionPrev_group.setShortcut(_translate("MainWindow", "`"))
        self.actionNext_group.setText(_translate("MainWindow", "Next group"))
        self.actionNext_group.setShortcut(_translate("MainWindow", "Ctrl+`"))
        self.actionRepaint.setText(_translate("MainWindow", "Repaint"))
        self.actionRepaint.setShortcut(_translate("MainWindow", "R"))
        self.actionScene_shot.setText(_translate("MainWindow", "Scene shot"))
        self.actionScene_shot.setShortcut(_translate("MainWindow", "P"))
        self.actionWindow_shot.setText(_translate("MainWindow", "Window shot"))
        self.actionWindow_shot.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionLanguage.setText(_translate("MainWindow", "Language"))
