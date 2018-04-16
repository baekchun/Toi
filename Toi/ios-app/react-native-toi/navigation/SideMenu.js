import PropTypes from "prop-types";
import React, { Component } from "react";
import { NavigationActions } from "react-navigation";
import {
  ScrollView,
  Text,
  View,
  Image,
  StyleSheet,
  TouchableOpacity
} from "react-native";
import Colors from "../constants/Colors";
import firebase from "firebase";

class SideMenu extends Component {
  navigateToScreen = route => () => {
    const navigateAction = NavigationActions.navigate({
      routeName: route
    });
    this.props.navigation.dispatch(navigateAction);
  };

  logout() {
    const resetAction = NavigationActions.reset({
      index: 0,
      actions: [NavigationActions.navigate({ routeName: "Main" })]
    });
    firebase
      .auth()
      .signOut()
      .then(() => this.props.navigation.dispatch(resetAction));
  }

  render() {
    return (
      <View style={styles.container}>
        <ScrollView>
          <View>
            <Image
              style={{
                width: 64,
                height: 64,
                borderRadius: 32,
                borderWidth: 2,
                borderColor: Colors.main
              }}
              source={require("../assets/images/face.png")}
            />
            <Text style={{ color: Colors.textBlack, marginTop: 16 }}>
              Welcome,{" "}
              <Text style={{ color: Colors.main, fontSize: 18 }}>Sung</Text>!
            </Text>

            <TouchableOpacity
              onPress={() => this.props.navigation.navigate("Docs")}
              style={{
                flexDirection: "row",
                alignItems: "center",
                marginTop: 24
              }}
            >
              <Image
                style={{ width: 24, height: 24 }}
                source={require("../assets/icons/icons8-document.png")}
              />
              <Text style={{ marginLeft: 4, fontSize: 16, color: Colors.text }}>
                My Data
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
        <View style={styles.footerContainer}>
          <TouchableOpacity
            onPress={() => this.logout()}
            hitSlop={{ top: 8, right: 8, left: 8, bottom: 8 }}
          >
            <Text style={{ color: Colors.main }}>LOG OUT</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }
}

SideMenu.propTypes = {
  navigation: PropTypes.object
};

const styles = StyleSheet.create({
  container: {
    paddingTop: 38,
    padding: 16,
    flex: 1
  },
  navItemStyle: {
    padding: 10
  },
  navSectionStyle: {
    backgroundColor: "lightgrey"
  },
  sectionHeadingStyle: {
    paddingVertical: 10,
    paddingHorizontal: 5
  },
  footerContainer: {}
});

export default SideMenu;
