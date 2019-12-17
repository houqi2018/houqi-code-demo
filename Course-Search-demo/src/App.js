import React from 'react';
import './App.css';
import Sidebar from './Sidebar';
import CourseArea from './CourseArea';
import Cart from './Cart';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      allCourses: {},
      filteredCourses: {},
      subjects: [],
      inCart:[],
      taken: {},    // Past courses
      untaken: {},  // Untaken courses
      mode: 1,  // Mode 1 is all, 2 is taken, 3 is recommended
      keywordsRanking: {},  // Used to sort courses
    };
  }
  async componentDidMount() {
    await fetch('https://www.houqi.li/639.json').then(
      res => res.json()
    ).then(data => {
      Object.keys(data).forEach(function(key) {
        data[key]["rating"] = 0;  // Add attributes "rating" and "likeOrDislike"
        data[key]["likeOrDislike"] = 0;
      });
      this.setState({allCourses: data, taken: data, filteredCourses: data, subjects: this.getSubjects(data)});
    })

    await fetch('https://mysqlcs639.cs.wisc.edu/students/5022025924/classes/completed').then(
      res => res.json()
    ).then(data => {
      let dict = this.state.allCourses;
      let takenResult = {};
      let untakenResult = {};
      Object.values(data)[0].forEach(function(abbr) {
        let temp = Object.keys(dict).reduce(function (filtered, key) {
              if (Object.values(data)[0].includes(key)) filtered[key] = dict[key];
              return filtered;
        }, {});
        let temp2 = Object.keys(dict).reduce(function (filtered, key) {
          if (!Object.values(data)[0].includes(key)) {
            filtered[key] = dict[key];
          }
          return filtered;
        }, {});
        takenResult = Object.assign({}, takenResult, temp);
        untakenResult = Object.assign({}, untakenResult, temp2);
        });
      this.setState({taken: takenResult});
      this.setState({untaken: untakenResult});
      // Update untaken rankings
      this.updateRating();
    });
  }
  
  updateRating () {
    this.updateKeywordsRating();
    this.updateUntakenRating();
  }

  updateKeywordsRating () {
    let keywordsRankingTemp = {};
    Object.values(this.state.allCourses).forEach(function(elt) {
      let keyword = elt["keywords"];
      keyword.forEach((curr) => {
        keywordsRankingTemp[curr] = 0;
      })
    });
    Object.values(this.state.taken).forEach(function(abbr) {
      let likeOrDislike = abbr["likeOrDislike"];
      let keyword = abbr["keywords"];
      keyword.forEach((curr) => {
        if (likeOrDislike === 2) {  // Dislike
          keywordsRankingTemp[curr] -= 1;
        }
        else if (likeOrDislike === 1) {  // Like
          keywordsRankingTemp[curr] += 1;
        }
      })
    });
    this.setState({keywordsRanking: keywordsRankingTemp});
  }
  
  updateUntakenRating () {
    let d = this.state.keywordsRanking;
    Object.values(this.state.untaken).forEach(function(elt) {
      let keywords = elt["keywords"];
      let weight = 0;
      keywords.forEach((curr) => {
        weight += d[curr];
      });
      elt["rating"] = weight;
    });
  }

  getSubjects(data) {
    let subjects = [];
    subjects.push("All");

    for(const course of Object.values(data)) {
      if(subjects.indexOf(course.subject) === -1)
        subjects.push(course.subject);
    }

    return subjects;
  }

  setCourses(courses) {
    this.setState({untaken: courses})
  }

  updateTaken(oneEntry) {
    let newtaken = this.state.taken;
    Object.keys(newtaken).forEach(function(key) {
      let cour = newtaken[key];
      if (cour["number"] === oneEntry["number"]) {
        newtaken[key] = oneEntry;
      }
    });
    this.setState({taken: newtaken});
    this.updateRating();
  }

  render() {
    return (
      <>
        <link
          rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
          crossOrigin="anonymous"
        />
       
        <Sidebar setCourses={(courses) => this.setCourses(courses)} untaken={this.state.untaken} courses={this.state.allCourses} subjects={this.state.subjects} mode={this.state.mode} modeCallback={(mode) => { this.setState({mode: mode}); this.updateRating(); }}/>
        <div style={{marginLeft: '20vw'}}>
          <CourseArea data={this.state.filteredCourses}  inCart={this.state.inCart} taken={this.state.taken} untaken={this.state.untaken} mode={this.state.mode} courseAreaCallback={(newCart) => { this.setState({inCart: newCart}) }} courseAreaCallbackForPastCourse={(oneEntry) => { this.updateTaken(oneEntry) }}/>
        </div>
        <Cart inCart={this.state.inCart} cartCallback={(newCart) => { this.setState({inCart: newCart}) }}/>
      </>
    )
  }
}

export default App;
