
// 引入coolsite360交互配置设定
require('coolsite.config.js');
// 获取全局应用程序实例对象
var app = getApp();

// 创建页面实例对象
Page({
  /**
   * 页面名称
   */
  name: "login",
  /**
   * 页面的初始数据
   */

  data: {
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad () {
    // 注册coolsite360交互模块
    app.coolsite360.register(this);

    
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

  getUserScope(){
    wx.getUserInfo({
      success(e){
        console.log(e)
        var name = e.userInfo.nickName
        var avatarurl = e.userInfo.avatarUrl
        wx.login({
          success(e){
            var code = e.code
            wx.request({
              url: "https://api.weixin.qq.com/sns/jscode2session?appid=" + "wx45895946db0d930a" + "&secret=" + "244f5905799e5334be4c203777c1ff5a"+"&js_code="+ code +"&grant_type=authorization_code",
              success(e){
                console.log(avatarurl)
                wx.request({
                  url: 'http://localhost:5000'+'/user/add',
                  method: "POST",
                  data:{
                    openid: e.data.openid,
                    name: name,
                    avatarurl: avatarurl 
                  },
                  header: {
                    'content-type': 'application/json' // 默认值
                  },
                  success(e){
                    console.log(e)
                    wx.navigateTo({
                      url: '../index/index'
                    })
                  }
                })
              }
            })
          }
        })
        
      }
    })
  },

  //以下为自定义点击事件
  goToDetail: function (e) {
    var ctid = e.target.dataset.ctid
    var that = this
    if (app.lid == '0') {
      wx.navigateTo({
        url: '../scene/scene?ctid=' + ctid,
      })
    } else {
      wx.navigateTo({
        url: '../fc/fc?ctid=' + ctid,
      })
    }

  }
})

