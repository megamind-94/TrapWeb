
// 引入coolsite360交互配置设定
require('coolsite.config.js');

// 获取全局应用程序实例对象
var app = getApp();

// 创建页面实例对象
Page({
  /**
   * 页面名称
   */
  name: "scene",
  /**
   * 页面的初始数据
   */

  data: {
    "title": "",
    "image": "",
    "title": "",
    "price": "",
    "time": "",
    "addr": "",
    "hotel_items": "",
    "food_items": "",
    "content": "",
    "jd": [],
    "ms": [],
    "currentTab": '0',
    "_h": "",
    "_w": "",
    "comments": [],
    "ctid": "",
    "input_text": "",
    "is_keep": false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad (options) {
    // 注册coolsite360交互模块
    app.coolsite360.register(this);
    var ctid = options.ctid
    this.data.ctid = ctid
    var that = this
    wx.request({
      url: 'http://localhost:5000'+'/contents',
      method: "POST",
      data: {
        "uid": app.uid,
        "ctid": ctid
      },
      success(e){
        var result = e.data.content
        that.setData({
          "title": result[0]['title'],
          "image": result[0]["coverid2"],
          "addr": result[0]["addr"],
          "content": result[0]["content"],
          "time": result[0]["time"],
          "price": result[0]["price"],
          "jd": result[0]["jd"],
          "ms": result[0]["ms"],
          "is_keep": result[0]['is_keep']
        })
        var i = '0'
        that.imageStyle(i)
      }
    })
    console.log(this)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow () {
    // 执行coolsite360交互组件展示
    app.coolsite360.onShow(this);
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh () {
    
  },


  //以下为自定义点击事件
  
  // tap_b4cfcca0:function(e){
  //   //触发coolsite360交互事件
  //   app.coolsite360.fireEvent(e,this);
  // },
  
  // tap_8667c3b4:function(e){
  //   //触发coolsite360交互事件
  //   app.coolsite360.fireEvent(e,this);
  // },
  
  // tap_04d11e14:function(e){
  //   //触发coolsite360交互事件
  //   app.coolsite360.fireEvent(e,this);
  // },
  
  // tap_5e0030d0:function(e){
  //   //触发coolsite360交互事件
  //   app.coolsite360.fireEvent(e,this);
  // },
  
  // tap_47a359d0:function(e){
  //   //触发coolsite360交互事件
  //   app.coolsite360.fireEvent(e,this);
  // },
  
  // tap_862c2db8:function(e){
  //   //触发coolsite360交互事件
  //   // app.coolsite360.fireEvent(e,this);
    
  // },

  swiper_change: function(e){
    this.setData({
      "currentTab": e.currentTarget.dataset.current_tab
    })
    if(e.currentTarget.dataset.current_tab == '2'){
      this.getComments(this.data.ctid)
    }
    this.imageStyle(e.currentTarget.dataset.current_tab)
  },
  stopTouchMove:function(e){
    return false
  },
  imageStyle(currentTab){
    var that = this
    if(currentTab == '0'){
      wx.getImageInfo({
        src: this.data.content,
        success: function(res){ 
          that.setData({
            "_h": res.height * wx.getSystemInfoSync().windowWidth / res.width,
            "_w": wx.getSystemInfoSync().windowWidth
          }) 
        }
      })
    }else if(currentTab == '1'){
      that.setData({
        "_h": that.data.jd.length * 200 + that.data.ms.length * 200 + 200,
        "_w": wx.getSystemInfoSync().windowWidth
      })
    }else{
        that.setData({
          "_h": that.data.comments.length * 100 + 100,
          "_w": wx.getSystemInfoSync().windowWidth
        })
    }
  },
  getComments(ctid){
    var that = this
    wx.request({
      url: 'http://localhost:5000' + '/comments/' + ctid,
      method: "GET",
      success(e){
        console.log(e)
        if(e.data.status == 1){
          that.setData({
            "comments": e.data.content
          })
        }else{
          that.setData({
            "comments": []
          })
        }
        
      }
    })
  },
  addComment(){
    var text = this.data.input_text
    var ctid = this.data.ctid
    if(app.uid == ""){
      wx.navigateTo({
        url: '../login/login',
      })
    }else{
      wx.request({
        url: 'http://localhost:5000' + '/comments/add',
        method: "POST",
        data: {
          "uid": app.uid,
          "text": text,
          "ctid": ctid
        }
      })
    }
  },

  inputChange(e){
    this.setData({
      input_text: e.detail.value
    })
  },

  changeKeep(e){
    var keepno = e.currentTarget.dataset.keepno
    var isKeep = this.data.is_keep
    var that = this
    if(keepno == '0'){
      wx.request({
        url: 'http://localhost:5000' + '/keeps/add',
        method: 'POST',
        data: {
          "uid": app.uid,
          "ctid": that.data.ctid
        },
        success(e){
          if(e.data.status == 1){
            that.setData({
              "is_keep": true
            })
          }
        }
      })
    }else{
      wx.request({
        url: 'http://localhost:5000' + '/keeps/del',
        method: 'POST',
        data: {
          "uid": app.uid,
          "ctid": that.data.ctid
        },
        success(e) {
          if (e.data.status == 1) {
            that.setData({
              "is_keep": false
            })
          }
        }
      })
    }
  }
})