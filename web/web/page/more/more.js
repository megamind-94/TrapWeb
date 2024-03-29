
// 引入coolsite360交互配置设定
require('coolsite.config.js');

// 获取全局应用程序实例对象
var app = getApp();

// 创建页面实例对象
Page({
  /**
   * 页面名称
   */
  name: "more",
  /**
   * 页面的初始数据
   */

  data: {
    "lists": ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad (options) {
    // 注册coolsite360交互模块
    app.coolsite360.register(this);
    var tid = options.tid
    var that = this
    wx.request({
      url: 'http://localhost:5000'+'/more/'+tid,
      method: 'GET',
      success(e){
        console.log(e)
        that.setData({
          "lists": e.data.content,
        })
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
  
  
  goToDetail: function(e){
    var ctid = e.currentTarget.dataset.ctid
    console.log(e)
    if(e.currentTarget.dataset.lid=='2'){
      wx.navigateTo({
        url: '../scene/scene?ctid=' + ctid,
      })
    }else{
      wx.navigateTo({
        url: '../fc/fc?ctid='+ctid,
      })
    }
    
  }
})

