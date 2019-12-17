import {createAppContainer, createSwitchNavigator} from 'react-navigation';
import {createStackNavigator} from 'react-navigation-stack';
import {createBottomTabNavigator} from 'react-navigation-tabs';
import Login from './Login';
import Signup from './Signup';
import Today from './Today';
import Settings from './Settings';
import Example from './Example';
import LoadingUpdateGoals from './LoadingUpdateGoals';
import LoadingToday from './LoadingToday';
import LoadingDailyActivity from './LoadingDailyActivity';
import LoadingActivity from './LoadingActivity';
import UpdateGoals from './UpdateGoals';
import Activity from './Activity';
import UpdateActivity from './UpdateActivity';
import UpdateActivityFinish from './UpdateActivityFinish';
import UpdateGoalsFinish from './UpdateGoalsFinish';

const AuthStack = createStackNavigator({
  Login: {
    screen: Login,
    navigationOptions: {
      headerTitle: 'Log In',
    },
  },
  Signup: {
    screen: Signup,
    navigationOptions: {
      headerTitle: 'Sign Up',
    },
  },
});

const TodayStack = createStackNavigator({
  Today: {
    screen: Today,
    navigationOptions: {
      headerTitle: 'Today',
    },
  },
  TodayDetails: {
    screen: Example,
    navigationOptions: {
      headerTitle: 'Details',
    },
  },
});

const TodaySwitch = createSwitchNavigator({
  LoadingToday: {
    screen: LoadingToday,
  },
  LoadingDailyActivity: {
    screen: LoadingDailyActivity,
  },
  TodayLoaded: {
    screen: TodayStack,
  },
});

const SettingsStack = createStackNavigator({
  Settings: {
    screen: Settings,
    navigationOptions: {
      headerTitle: 'Settings',
    },
  },
});

const SettingsSwitch = createSwitchNavigator({
  SettingsLoaded: {
    screen: SettingsStack,
  },
  LoadingUpdateGoals: {
    screen: LoadingUpdateGoals,
  },
  UpdateGoals: {
    screen: UpdateGoals,
    navigationOptions: {
      headerTitle: 'Update Goals',
    },
  },
  UpdateGoalsFinish: {
    screen: UpdateGoalsFinish,
  },
});

const ActivityStack = createStackNavigator({
  Activity: {
    screen: Activity,
    navigationOptions: {
      headerTitle: 'Activities',
    },
  },
});

const ActivitySwitch = createSwitchNavigator({
  LoadingActivity: {
    screen: LoadingActivity,
  },
  ActivityLoaded: {
    screen: ActivityStack,
  },
  UpdateActivity: {
    screen: UpdateActivity,
    navigationOptions: {
      headerTitle: 'Update Goals',
    },
  },
  UpdateActivityFinish: {
    screen: UpdateActivityFinish,
  },
});

const MainTabs = createBottomTabNavigator({
  Today: {
    screen: TodaySwitch,
    navigationOptions: {
      tabBarLabel: 'Today',
    },
  },
  Activity: {
    screen: ActivitySwitch,
    navigationOptions: {
      tabBarLabel: 'Activities',
    },
  },
  Settings: {
    screen: SettingsSwitch,
    navigationOptions: {
      tabBarLabel: 'Settings',
    },
  },
});

const App = createSwitchNavigator({
  Auth: {
    screen: AuthStack,
  },
  App: {
    screen: MainTabs,
  },
});

export default createAppContainer(App);