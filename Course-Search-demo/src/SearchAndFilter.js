class SearchAndFilter {
  searchAndFilter(untaken, currTag) {
    let filtered = Object.entries(untaken).filter(([key,cour]) => {
      return currTag.length === 0 ? untaken : cour['keywords'].some(tag => {
        return currTag.includes(tag)
    })});
    filtered.sort((a, b) => (a[1].rating > b[1].rating) ? -1 : 1);
    var result = filtered.reduce(function(map, obj) {
      map[obj[0]] = obj[1];
      return map;
    }, {});
    return result;
  }
}

export default SearchAndFilter;