
// 引入coolsite360交互配置设定
require('coolsite.config.js');

// 获取全局应用程序实例对象
var app = getApp();

// 创建页面实例对象
Page({
  /**
   * 页面名称
   */
  name: "user",
  /**
   * 页面的初始数据
   */

  data: {
    "results": [],
    "currentTab": "",
    "nickname": "",
    "face": ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad () {
    // 注册coolsite360交互模块
    app.coolsite360.register(this);
    var that = this
    wx.getSetting({
      success(e){
        if(!e.authSetting['scope.userInfo']){
          wx.navigateTo({
            url: '../login/login',
          })
        }else{
          wx.getUserInfo({
            success(e) {
              that.setData({
                'nickname': e.userInfo.nickName,
                'face': e.userInfo.avatarUrl
              })
              if(app.uid == ""){
                that.getUserScope()
              }
              // that.changeTab({ target: { dataset: { current_tab: 0 } } })
            }
          })
        }
      }
    })
    
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
  changeTab: function(e){
    var that = this
    var current = e.target.dataset.current_tab
    var url = ""
    if(current == "0"){
      url = "http://localhost:5000"+"/history/"+app.uid
    }else{
      url = "http://localhost:5000"+"/keeps/"+app.uid
    }

    wx.request({
      url: url,
      success(e){
        if(e.data.status == 1){
          that.setData({
            "results": e.data.content.details
          })
        }else{
          that.setData({
            "results": []
          })
        }
      }
    })
    that.setData({
      "currentTab": current
    })
  },
  
  goToDetail: function (e) {
    var ctid = e.currentTarget.dataset.ctid
    var lid = e.currentTarget.dataset.lid
    this.add_history(ctid)
    var that = this
    if (lid == '2') {
      wx.navigateTo({
        url: '../scene/scene?ctid=' + ctid,
      })
    } else {
      wx.navigateTo({
        url: '../fc/fc?ctid=' + ctid,
      })
    }
  },
  getUserScope() {
    var that = this
        wx.login({
          success(e) {
            var code = e.code
            wx.request({
              url: "https://api.weixin.qq.com/sns/jscode2session?appid=" + "wx2ed99e00d8f6e684" + "&secret=" + "7953c7df51cded0d887b34bcc79ed3c8" + "&js_code=" + code + "&grant_type=authorization_code",
              success(e) {
                app.uid = e.data.openid
              }
            })
      }
    })
  },
  add_history(ctid) {
    wx.request({
      url: 'http://localhost:5000' + '/historys/add',
      method: 'POST',
      data: {
        'ctid': ctid,
        'uid': app.uid
      }
    })
  }
})

