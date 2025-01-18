require 'httparty'
require 'nokogiri'
require 'json'
require 'csv'
require 'fileutils'

ciudades = ["southwark-85215", "london-87490" ]

def scrape_page(city, page_number)
  url = "https://www.rightmove.co.uk/house-prices/#{city}.html?pageNumber=#{page_number}"

  response = HTTParty.get(url)

  parsed_page = Nokogiri::HTML(response.body)

  script_content = parsed_page.xpath('//script[contains(text(), "window.PAGE_MODEL")]').first&.text&.strip
  return nil if script_content.nil?

  json_data = script_content.match(/window.PAGE_MODEL = (\{.*?\});/m)[1]
  JSON.parse(json_data)["searchResult"]["properties"]
end

ciudades.each do |ciudad|
  puts "Comenzando a raspar datos para: #{ciudad}"
  all_properties = []

  FileUtils.mkdir_p("dataAnalysis/datos/json/#{ciudad}")
  FileUtils.mkdir_p("dataAnalysis/datos/csv/#{ciudad}")

  (1..40).each do |page_number|
    properties = scrape_page(ciudad, page_number)
    break if properties.nil?

    all_properties.concat(properties)
    puts "Página #{page_number} de #{ciudad} raspada con éxito."
  end


  File.open("dataAnalysis/datos/json/#{ciudad}/data.json", "w") do |f|
    f.write(JSON.pretty_generate(all_properties))
  end


  CSV.open("dataAnalysis/datos/csv/#{ciudad}/data.csv", "wb") do |csv|
    csv << ["Address", "Property Type", "Bedrooms", "Main Image URL", "Detail URL", "Display Price", "Date Sold"]
    all_properties.each do |property|
      property["transactions"].each do |transaction|
        csv << [
          property["address"],
          property["propertyType"],
          property["bedrooms"],
          property["imageInfo"] ? property["imageInfo"]["imageUrl"] : nil,
          property["detailUrl"],
          transaction["displayPrice"],
          transaction["dateSold"]
        ]
      end
    end
  end

  puts "Datos guardados en archivos para #{ciudad}."
end
