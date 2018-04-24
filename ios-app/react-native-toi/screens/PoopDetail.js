import React, { Component } from "react";
import {
  Animated,
  View,
  Dimensions,
  Image,
  Text,
  StyleSheet,
  ScrollView,
  TouchableWithoutFeedback
} from "react-native";
import moment from "moment";
import Colors from "../constants/Colors";

const { width, height } = Dimensions.get("window");
const POOPS = [
  require("../assets/poops/type1.png"),
  require("../assets/poops/type2.png"),
  require("../assets/poops/type3.png"),
  require("../assets/poops/type4.png"),
  require("../assets/poops/type5.png"),
  require("../assets/poops/type6.png"),
  require("../assets/poops/type7.png")
];

const POOP_DETAIL = {
  1: {
    description: `You're lacking fiber and fluids. Drink more water and chomp on some fruits and veggies.`,
    images: [
      require("../assets/icons/icons8-man_drinking_water.png"),
      require("../assets/icons/icons8-asparagus.png")
    ]
  },
  2: {
    description: `Not as serious as separate hard lumps, but you need to load up on fluids and fiber.`,
    images: [
      require("../assets/icons/icons8-porridge.png"),
      require("../assets/icons/icons8-water.png"),
      require("../assets/icons/icons8-peas.png")
    ]
  },
  3: {
    description: `This is normal, but the cracks mean you could still up your intake of water`,
    images: [require("../assets/icons/icons8-water.png")]
  },
  4: {
    description: `Optimal poop! You're doing fine.`,
    images: [require("../assets/icons/icons8-hearts.png")]
  },
  5: {
    description: `Not too bad. Pretty normal if you poop multiple times a day.`,
    images: [require("../assets/icons/icons8-happy.png")]
  },
  6: {
    description: `You're on the edge of normal. This type of poop is on its way of becoming a diarrhea`,
    images: [require("../assets/icons/icons8-neutral_emoticon.png")]
  },
  7: {
    description: `You're having a diarrhea. This is probably caused by some sort of infection and diarrhea is your body's way of cleaning it out. Make sure you drink lots of fluid to replace the lost fluid in your body--or you might find yourself dehydrated!`,
    images: [
      require("../assets/icons/icons8-water.png"),
      require("../assets/icons/icons8-man_drinking_water.png")
    ]
  }
};

export default class PoopDetail extends Component {
  static navigationOptions = {
    title: "Stool Details"
  };

  constructor(props) {
    super(props);
    this.state = {
      opacity: new Animated.Value(1),
      ...props.navigation.state.params.data
    };
  }

  reveal() {
    Animated.timing(this.state.opacity, { toValue: 0, duration: 1500 }).start();
  }

  renderWarning() {
    const { contains_blood, contains_mucus } = this.state;
    if (contains_blood || contains_mucus) {
      return (
        <View
          style={{
            padding: 16,
            marginHorizontal: 16,
            marginVertical: 8,
            backgroundColor: "white",
            borderRadius: 8
          }}
        >
          <Text style={{ fontWeight: "700", color: "#F44336" }}>Warning</Text>
          <View
            style={{
              flexDirection: "row",
              justifyContent: "center",
              marginTop: 16
            }}
          >
            {contains_blood && (
              <View style={{ alignItems: "center", marginHorizontal: 8 }}>
                <Image
                  style={{ width: 48, height: 48 }}
                  source={require("../assets/icons/icons8-drop_of_blood.png")}
                />
                <Text style={{ color: "gray", marginTop: 8, fontSize: 12 }}>
                  Blood Found
                </Text>
              </View>
            )}
            {contains_mucus && (
              <View style={{ alignItems: "center", marginHorizontal: 8 }}>
                <Image
                  style={{ width: 48, height: 48 }}
                  source={require("../assets/icons/icons8-booger.png")}
                />
                <Text style={{ color: "gray", marginTop: 8, fontSize: 12 }}>
                  Mucus Found
                </Text>
              </View>
            )}
          </View>
        </View>
      );
    }
  }

  renderInfo() {
    const { bristol_type, date } = this.state;
    return (
      <View style={{ padding: 16 }}>
        <Text style={{ fontSize: 24, fontWeight: "600" }}>
          Stool Type {bristol_type}
        </Text>
        <Text style={{ color: "gray" }}>
          {moment(date).format("MMM Do YY")}
        </Text>
      </View>
    );
  }

  renderChart() {
    const { bristol_type } = this.state;
    return (
      <View
        style={{
          padding: 16,
          margin: 16,
          borderRadius: 8,
          backgroundColor: "white",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "space-between"
        }}
      >
        {POOPS.map((p, i) => {
          let extraView = {};
          let extraText = {};
          if (i == bristol_type - 1) {
            extraView = {
              backgroundColor: Colors.main,
              borderRadius: 40,
              padding: 10
            };
            extraText = { color: "white", fontWeight: "700" };
          }
          return (
            <View key={i} style={[{ alignItems: "center" }, extraView]}>
              <Image style={{ width: 24, height: 24 }} source={POOPS[i]} />
              <Text style={[{ color: "gray", fontSize: 10 }, extraText]}>
                Type {i + 1}
              </Text>
            </View>
          );
        })}
      </View>
    );
  }

  renderRecommendation() {
    //debug
    const { bristol_type } = this.state;
    return (
      <View
        style={{
          padding: 16,
          marginHorizontal: 16,
          marginVertical: 8,
          borderRadius: 8,
          backgroundColor: "white"
        }}
      >
        <View style={{ flexDirection: "row", alignSelf: "center" }}>
          {POOP_DETAIL[bristol_type].images.map((image, i) => (
            <Image
              key={i}
              style={{ width: 36, height: 36, marginHorizontal: 4 }}
              source={image}
            />
          ))}
        </View>
        <Text style={{ color: "#7d7d7d", fontSize: 12, marginTop: 16 }}>
          {POOP_DETAIL[bristol_type].description}
        </Text>
      </View>
    );
  }

  renderPreview() {
    const { opacity, bristol_type } = this.state;
    return (
      <TouchableWithoutFeedback
        onPress={() => this.reveal()}
        style={[styles.image]}
      >
        <View style={{ alignSelf: "center", marginVertical: 16 }}>
          <Image
            style={styles.image}
            resizeMode={"contain"}
            source={require("../assets/poops/blood.jpeg")}
          />
          <Animated.View
            style={[
              styles.image,
              {
                position: "absolute",
                left: 0,
                top: 0,
                backgroundColor: "rgba(0,0,0,.97)",
                alignItems: "center",
                justifyContent: "center",
                opacity
              }
            ]}
          >
            <Image
              source={require("../assets/icons/icons8-unlock.png")}
              style={{ width: 48, height: 48 }}
            />
            <Text style={{ color: "white", marginTop: 16 }}>
              Tap to Reveal the Image
            </Text>
          </Animated.View>
        </View>
      </TouchableWithoutFeedback>
    );
  }

  renderBar() {
    const { bar_chart, color_distribution } = this.state;
    const b64 = `data:image/png;base64,${bar_chart}`;
    const obj = JSON.parse(color_distribution);
    return (
      <View
        style={{
          padding: 16,
          marginHorizontal: 16,
          marginVertical: 8,
          backgroundColor: "white",
          borderRadius: 8,
          justifyContent: "center"
        }}
      >
        <Image
          resizeMode={"contain"}
          style={{ height: 50, width: width - 64 }}
          source={{ uri: b64 }}
        />

        <View style={{ marginVertical: 16, paddingHorizontal: 64 }}>
          {Object.keys(obj).map((o, i) => {
            return (
              <View
                key={i}
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between"
                }}
              >
                <Text style={{ fontWeight: "600" }}>{o}</Text>
                <Text style={{ color: "gray" }}>
                  {Number(obj[o]).toFixed(3)}%
                </Text>
              </View>
            );
          })}
        </View>
      </View>
    );
  }

  render() {
    return (
      <ScrollView style={{ flex: 1 }}>
        {this.renderInfo()}
        {this.renderWarning()}
        {this.renderChart()}
        {this.renderRecommendation()}
        {this.renderBar()}
        {this.renderPreview()}
      </ScrollView>
    );
  }
}

const styles = StyleSheet.create({
  image: {
    width: width - 32,
    height: 300,
    borderRadius: 16
  }
});
