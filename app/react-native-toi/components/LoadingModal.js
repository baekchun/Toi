import React from "react";
import { Dimensions, StyleSheet, Modal, View, Text } from "react-native";
import { DangerZone } from "expo";
const { Lottie } = DangerZone;
const { width, height } = Dimensions.get("window");

export default class LoadingModal extends React.Component {
  state = {
    animation: require("../lottie/preloader.json")
  };

  _playAnimation() {
    if (this.animation) {
      this.animation.play();
    }
  }

  componentWillUnmount() {
    if (this.animation) {
      this.animation.reset();
    }
  }

  render() {
    const { visible } = this.props;

    return (
      <Modal
        onShow={() => {
          this._playAnimation();
        }}
        animationType="fade"
        visible={visible}
        transparent={true}
        style={styles.container}
        onRequestClose={() => this.setState({ visible: false })}
      >
        <View
          style={{
            flex: 1,
            backgroundColor: "rgba(0,0,0,.8)",
            justifyContent: "center",
            alignItems: "center"
          }}
        >
          <View>
            <Lottie
              loop
              ref={animation => {
                this.animation = animation;
              }}
              style={{
                width: 200,
                height: 200
              }}
              source={this.state.animation}
            />
          </View>
        </View>
      </Modal>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  }
});
