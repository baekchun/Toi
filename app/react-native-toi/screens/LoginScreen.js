import React, { Component } from "react";
import {
  View,
  Image,
  Text,
  TextInput,
  ImageBackground,
  StatusBar,
  StyleSheet
} from "react-native";

import { IconTextInput, Button } from "../components";
import Colors from "../constants/Colors";
import * as Animatable from "react-native-animatable";

const ICON_SIZE = 80;

export default class Login extends Component {
  static navigationOptions = {
    header: null
  };

  render() {
    return (
      <View style={{ flex: 1 }}>
        <StatusBar barStyle="light-content" />
        <ImageBackground
          style={{ flex: 1 }}
          source={require("../assets/images/bath_bg.jpg")}
        >
          <View
            style={{
              flex: 1,
              backgroundColor: "rgba(0,0,0,.7)"
            }}
          >
            <View
              style={{
                flex: 1,
                justifyContent: "center",
                alignItems: "center"
              }}
            >
              <Animatable.Image
                animation={"fadeIn"}
                duration={1500}
                delay={500}
                style={{
                  width: ICON_SIZE,
                  height: ICON_SIZE,
                  marginBottom: 24
                }}
                source={require("../assets/images/toi-logo.png")}
              />
              <Animatable.View animation='fadeInUp' duration={1000} delay={800}>
              <Text style={{ color: "white", fontSize: 32, fontWeight: "600" }}>
                ToI
              </Text>

              </Animatable.View>

              <Animatable.View animation='fadeInUp' duration={1000} delay={1600}>
                <IconTextInput
                  icon={require("../assets/icons/icons8-user_filled.png")}
                  placeholder={"Username"}
                />
                <IconTextInput
                  icon={require("../assets/icons/icons8-lock.png")}
                  placeholder={"Password"}
                />
              </Animatable.View>
            </View>
                <Animatable.View animation='slideInUp' duration={1000} delay={2400}>
            <Button backgroundColor={Colors.main} text="Log In" />

                </Animatable.View>
          </View>
        </ImageBackground>
      </View>
    );
  }
}
