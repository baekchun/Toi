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

import { IconTextInput, Button, LoadingModal } from "../components";
import Colors from "../constants/Colors";
import * as Animatable from "react-native-animatable";
import firebase from "firebase";
import { NavigationActions } from "react-navigation";

const ICON_SIZE = 80;

export default class Login extends Component {
  static navigationOptions = {
    header: null
  };

  state = {
    loading: false
  };

  componentDidMount() {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        this.setState({ loading: false }, () => {
          this.reset(this.props.navigation, "Home", {});
        });
      } else {
        // No user is signed in.
        console.log("logged out");
      }
    });

    //test
    this.username.setText("sungwoo@mail.com");
    this.password.setText("sungwootest");
  }

  reset = (navigation, routeName, params = {}) => {
    const resetAction = NavigationActions.reset({
      index: 0,
      actions: [NavigationActions.navigate({ routeName, params })]
    });

    navigation.dispatch(resetAction);
  };

  login() {
    this.setState({ loading: true });
    const email = this.username.getText();
    const password = this.username.getText();

    firebase
      .auth()
      .createUserWithEmailAndPassword(email, password)
      .then(() => {
        this.setState({ loading: false }, () => {
          this.reset(this.props.navigation, "Home", {});
        });
      })
      .catch(error => {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode);
        if (errorCode == "auth/email-already-in-use") {
          firebase
            .auth()
            .signInWithEmailAndPassword(email, password)
            .then(() => {
              this.setState({ loading: false }, () => {
                this.reset(this.props.navigation, "Home", {});
              });
            })
            .catch(error => {
              var errorCode = error.code;
              var errorMessage = error.message;
              console.log(errorCode, errorMessage);
              this.setState({ loading: false });
            });
        }
      });
  }

  render() {
    const { loading } = this.state;
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
              <Animatable.View animation="fadeInUp" duration={1000} delay={800}>
                <Text
                  style={{ color: "white", fontSize: 32, fontWeight: "600" }}
                >
                  ToI
                </Text>
              </Animatable.View>

              <Animatable.View
                animation="fadeInUp"
                duration={1000}
                delay={1600}
              >
                <IconTextInput
                  ref={u => (this.username = u)}
                  icon={require("../assets/icons/icons8-user_filled.png")}
                  placeholder={"Username"}
                />
                <IconTextInput
                  ref={p => (this.password = p)}
                  icon={require("../assets/icons/icons8-lock.png")}
                  placeholder={"Password"}
                  secureTextEntry={true}
                />
              </Animatable.View>
            </View>
            <Animatable.View animation="slideInUp" duration={1000} delay={2400}>
              <Button
                onPress={() => this.login()}
                backgroundColor={Colors.main}
                text="Sign Up / Log In"
              />
            </Animatable.View>
          </View>
        </ImageBackground>
        <LoadingModal visible={loading} />
      </View>
    );
  }
}
