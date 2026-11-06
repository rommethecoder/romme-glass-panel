import QtQuick
import QtQuick.Window
import org.kde.ksvg as KSvg
Window {
    visible: true
    width: 480
    height: 120
    color: "#704050"
    KSvg.FrameSvgItem {
        id: frame
        anchors.centerIn: parent
        width: 420
        height: 72
        imagePath: Qt.resolvedUrl("../theme/widgets/panel-background.svg")
    }
    Timer {
        interval: 400
        running: true
        onTriggered: {
            if (frame.margins.left <= 0 || frame.margins.top <= 0) {
                console.error("Frame margins missing"); Qt.exit(1); return;
            }
            console.log("Frame loaded", frame.width, frame.height, "margins", frame.margins.left, frame.margins.top);
            Qt.quit();
        }
    }
}
